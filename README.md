# Cricket AI - Automated Commentary System

A comprehensive AI-powered cricket analysis and commentary generation system.

## Features

- **Multi-Model Detection**: YOLOv8, NanoDet, and Deformable DETR for robust object detection
- **Real-time Tracking**: ByteTrack and Kalman filtering for player and ball tracking
- **Event Detection**: Automated detection of runs, wickets, boundaries, and other cricket events
- **Pose Estimation**: MediaPipe-based pose analysis for bat-ball contact detection
- **LLM Commentary**: AI-generated cricket commentary with personalization
- **Text-to-Speech**: Natural voice synthesis for automated commentary
- **OCR Integration**: Scoreboard and jersey number recognition

## Project Structure

```
cricket-ai/
├── data/          # Dataset storage
├── models/        # Model weights
├── src/           # Source code
├── notebooks/     # Jupyter notebooks
├── scripts/       # Utility scripts
├── configs/       # Configuration files
├── logs/          # Application logs
├── docker/        # Docker configuration
└── tests/         # Unit tests
```

## Installation

### Quick Start (Windows with WSL)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add sample video:**
   - Place a cricket video file at `data/samples/sample.mp4`
   - See `data/samples/README.md` for instructions

3. **Run the test pipeline:**
   ```bash
   python src/pipeline/realtime_pipeline.py
   ```
   - Press 'q' to quit the video window

### Full Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the real-time demo:

```bash
bash scripts/run_realtime_demo.sh
```

## Docker

Build and run with Docker:

```bash
cd docker
docker-compose up
```

## License

MIT License
