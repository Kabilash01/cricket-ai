# Cricket AI - Setup Guide

## 🚀 Quick Start

This guide will help you set up the Cricket AI project from scratch.

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional)
- WSL2 (for Windows users) or Linux/macOS

## 🔧 Step 1: Install Dependencies

Run the following command in your project root:

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- opencv-python (computer vision)
- ultralytics (YOLOv8)
- numpy, pandas (data processing)
- filterpy (Kalman filtering)
- ensemble-boxes (box fusion)
- mediapipe (pose estimation)
- And more...

## ✅ Step 2: Verify Setup

Run the verification script to check your environment:

```bash
python verify_setup.py
```

This will check:
- ✅ All required Python packages
- ✅ Project directory structure
- ✅ Sample video file (if available)

## 🎥 Step 3: Add Sample Video

To test the pipeline, you need a cricket video:

1. Place a cricket video at: `data/samples/sample.mp4`
2. You can:
   - Download a cricket clip from YouTube
   - Use your own cricket footage
   - Use any cricket match video

## 🧪 Step 4: Run Test Pipeline

Once you have a sample video, run the test pipeline:

```bash
python src/pipeline/realtime_pipeline.py
```

This will:
- Read frames from your sample video
- Draw placeholder detection boxes
- Display the video in a window
- Press 'q' to quit

## 📁 Project Structure

```
cricket-ai/
├── src/
│   ├── ingest/           # Video reading/writing
│   │   └── video_reader.py
│   ├── vision/
│   │   ├── detectors/    # Object detection models
│   │   │   └── yolov8_detector.py
│   │   ├── fusion/       # Detection fusion
│   │   │   └── wbf_fusion.py
│   │   └── tracking/     # Object tracking
│   │       └── ball_kalman.py
│   ├── events/           # Event detection
│   │   └── event_schema.py
│   ├── llm/             # Commentary generation
│   │   └── template.py
│   ├── ui/              # Visualization
│   │   └── overlay.py
│   ├── pipeline/        # Main pipeline
│   │   └── realtime_pipeline.py
│   └── utils/           # Utilities
│       ├── config.py
│       └── logger.py
├── data/
│   └── samples/         # Sample videos
├── models/              # Model weights
├── configs/             # Configuration files
└── logs/               # Application logs
```

## 🐛 Troubleshooting

### Import Errors

If you get import errors when running the pipeline:

```bash
# Make sure you're in the project root directory
cd cricket-ai

# Add the src directory to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"  # Linux/Mac/WSL
set PYTHONPATH=%PYTHONPATH%;%CD%\src          # Windows CMD
```

Or modify the pipeline script to add the path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### OpenCV Display Issues

If the video window doesn't appear:

**On WSL:**
```bash
# Install VcXsrv or X410 for Windows
# Set DISPLAY environment variable
export DISPLAY=:0
```

**On headless servers:**
- The display functionality won't work
- You'll need to save frames to files instead

### Missing Sample Video

If you don't have a cricket video:
- The pipeline will fail with a file not found error
- See `data/samples/README.md` for instructions
- You can also modify `realtime_pipeline.py` to use a webcam:
  ```python
  reader = VideoReader(0)  # Use webcam instead of file
  ```

## 🎯 Next Steps

Once the basic pipeline is running:

1. **Download Model Weights**: Get pre-trained YOLOv8 models
2. **Configure Models**: Edit configs in `configs/`
3. **Implement Detection**: Replace placeholder boxes with real detections
4. **Add Tracking**: Implement player and ball tracking
5. **Event Detection**: Add logic for runs, wickets, boundaries
6. **LLM Commentary**: Integrate commentary generation
7. **TTS**: Add text-to-speech for voice commentary

## 📚 Additional Resources

- See individual module READMEs for detailed documentation
- Check `notebooks/` for Jupyter notebook tutorials
- Review `configs/` for model configurations
- Explore `tests/` for unit test examples

## 💡 Tips

- Start small: Get basic video reading working first
- Test modules individually before integrating
- Use the verification script regularly
- Check logs in `logs/` for debugging
- Keep your sample videos small (< 1 minute) for faster testing

---

**Ready to build?** Run `python verify_setup.py` to get started! 🚀
