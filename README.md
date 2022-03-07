# video-deep-fryer

Wrapper for ```ffmpeg``` to automatically deep fry videos and its related audio.

# usage
```python fry.py -iv sample.mp4 -o output.mp4 -nv 10 -na 5 -ne 20 ```

# Arguments 

Arg | Description | Default
:------- | :---------- | :----------
--input\_video, -iv | Video to run through deep fryer | NA
--input\_audio, -ia | Audio to replace video audio with to run through deep fryer | NA
--output\_file, -o | File path to save deep fried video | NA
--n\_video, -nv | number of times to process the video | 2
--n\_audio, -na | number of times to process the audio | 1
--n\_emojis, -ne | number of emojis to add | 20
