from .auto_video_cut import Video
from os.path import dirname, abspath, join, basename


def main():
    '''
    Choose video file via file picker interface and save the
    resulting cut video to the same directory it is chosen from
    with '-output' suffix.
    '''
    video = Video.initViaFilePicker()
    videoParentPath = dirname(dirname(abspath(video.path)))
    videoName = basename(video.path)
    videoNamePartition = list(videoName.rpartition('.'))
    videoNamePartition.insert(1, '-output')
    outputVideoName = ''.join(videoNamePartition)
    outputVideoPath = join(videoParentPath, outputVideoName)
    video.autoCut(outputVideoPath)


main()
