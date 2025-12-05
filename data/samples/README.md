# Sample Data Directory

## Setup Instructions

To test the pipeline, place a sample cricket video file here named `sample.mp4`.

You can:
1. Download a cricket match clip from YouTube
2. Use any cricket footage you have
3. Create a short test video

The video should contain cricket gameplay for best results.

## Expected File
- `sample.mp4` - Your cricket video file

Once the video is in place, you can run:
```
python src/pipeline/realtime_pipeline.py
```

This will process the video and display frames with detection boxes (currently placeholder boxes).
