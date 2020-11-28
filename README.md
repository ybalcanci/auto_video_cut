# auto_video_cut
Creates a new video by cutting some portions of a given video according to the
sound volume level and the level's continuity. I.e. in order for a part of the video
to be taken off, it's sound volume must be under a threshold for a while.

## Example
```python
from auto_video_cut import Video

video = Video('sample.mp4')
video.autoCut('sample-out.mp4')
```
## Demo
[Auto Video Cut Demo (auto_video_cut)](https://www.youtube.com/watch?v=K3UMgwTyAAs)
