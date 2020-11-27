import soundfile
import moviepy.editor
import os.path
import logging
import wave
import tempfile
import shutil
import numpy as np

logger = logging.getLogger(__name__)


class Video:
    '''
    Represents a video, some portions of which will be cut off.
    '''
    
    def __init__(self, path):
        self.path = path
        self.video = moviepy.editor.VideoFileClip(path)
        self.audio = self.video.audio
        self._tmpAudioFileName = 'temp.wav'
        self._audioPath = None

    def autoCut(self, outputPath: str='./output.mp4'):
        '''
        Creates a new video by cutting some portions of the current video according to the
        sound volume level and the level's continuity. I.e. in order for a part of the video
        to be taken off, it's sound volume must be under a threshold and keep silent
        for a while.
        
        :param outputPath: Path to write the resulting video to.
        '''
        try:
            with tempfile.TemporaryDirectory() as tmpDir:
                self._audioPath = os.path.join(tmpDir, self._tmpAudioFileName)
                
                # create audio file
                self.audio.write_audiofile(self._audioPath)
                
                # get an array of sound volume values in the video
                soundArr = self._extractVolumeArray()

                # calculate duration using soundfile.SoundFile
                audioSoundFile = soundfile.SoundFile(self._audioPath, mode='rb')
                duration = len(audioSoundFile) / audioSoundFile.samplerate
        except Exception:
            try:
                shutil.rmtree(tmpDir)
            except Exception:
                pass

            
        cropPoints = self._calculateCropPoints(soundArr)
        processedCropPoints = self._processCropPoints(cropPoints, duration, len(soundArr))
        self._writeNewVideo(processedCropPoints, outputPath)

    def _writeNewVideo(self, cropPoints, outputVideoPath):
        clip = moviepy.editor.VideoFileClip(self.path)
        for start, end in cropPoints:
            clip = clip.cutout(start, end)
        clip.write_videofile(outputVideoPath)
    
    def _calculateCropPoints(self, arr):

        # min number of neighboring elements satisfying lowness that is required
        # for a portion to be cut off
        CROP_LENGTH_THRESHOLD = 20000

        # max number of neighboring elements NOT satisfying lowness required in a
        # series of satisfying elements that will not prevent the cut off.
        # For example, when 5000 elements are below the volumeThreshold, next 100 elements
        # are above it and 15000 more elements are below the volumeThreshold again;
        # the ones above are ignored and the portion is cut off.
        IGNORE_CONSTANT = 1000
        res = []
        mean = np.mean(arr)
        volumeThreshold = mean + 100
        firstOneMarked = False
        consecutiveness = 0
        first = None
        ignoredCount = 0
        for i, elm in enumerate(arr):
            if elm <= volumeThreshold:
                if not firstOneMarked:
                    first = i
                    firstOneMarked = True
                else:
                    consecutiveness += 1
            else:
                if consecutiveness > CROP_LENGTH_THRESHOLD:
                    res.append((first, i))
                    ignoredCount = 0
                    consecutiveness = 0
                    firstOneMarked = False
                elif ignoredCount <= IGNORE_CONSTANT:
                    consecutiveness += 1
                    ignoredCount += 1
                else:
                    ignoredCount = 0
                    firstOneMarked = False
                    consecutiveness = 0
        if firstOneMarked:
            res.append((first, i))
        return res
        
    def _processCropPoints(self, cropPoints, duration, soundArrLength):
        processedCropPoints = [(duration * a / soundArrLength, duration * b / soundArrLength)
                               for a, b in cropPoints]
        processedCropPoints = [(float('{:.3f}'.format(a)), float('{:.3f}'.format(b)))
                               for a, b in processedCropPoints]
        for i, (a, b) in enumerate(processedCropPoints, 1):
            dur = b - a
            while i < len(processedCropPoints):
                processedCropPoints[i] = (processedCropPoints[i][0] - dur,
                                          processedCropPoints[i][1] - dur)
                i += 1
        return processedCropPoints
    
    def _extractVolumeArray(self):
        w = wave.open(self._audioPath, "rb")
        p = w.getparams()
        f = p[3]  # number of frames
        s = w.readframes(f)
        s = np.fromstring(s, np.int16) / 10 * 5
        w.close()
        return s
