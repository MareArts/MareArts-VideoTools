# YouTube Video Resizer

## Overview
This project provides a toolset for downloading YouTube videos and converting them to a 16:9 aspect ratio. It includes two main scripts:

1. **`download_youtube.py`** - Downloads videos from YouTube.
2. **`16_9_video_gen.py`** - Converts videos to a 16:9 aspect ratio.

## Features
- Download YouTube videos using a URL.
- Resize videos while maintaining quality.
- Automatically adjust black bars or crop videos to fit 16:9.
- Output in standard video formats.

## Requirements
Make sure you have Python installed along with the necessary dependencies.

### Install dependencies
```bash
pip install -r requirements.txt
```

## Usage
### 1. Download a YouTube Video
```bash
python download_youtube.py <YouTube_URL>
```
This will save the video locally.

### 2. Convert Video to 16:9
```bash
python 16_9_video_gen.py <input_video> <output_video>
```
This will process the video and output a 16:9 formatted version.

## Dependencies
The project requires the following Python libraries:
- `pytube` (for downloading YouTube videos)
- `ffmpeg` (for video processing)
- `opencv-python` (for video handling)

You can install them manually if not using `requirements.txt`:
```bash
pip install pytube opencv-python ffmpeg-python
```

## License
This project is open-source under the MIT License.

## Author
MareArts
