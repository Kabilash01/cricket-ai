"""
Environment verification script for Cricket AI project.
Run this to check if all dependencies are properly installed.
"""

import sys

def check_imports():
    """Check if all required packages can be imported."""
    required_packages = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'ultralytics': 'ultralytics',
        'mediapipe': 'mediapipe',
        'filterpy': 'filterpy',
        'ensemble_boxes': 'ensemble-boxes',
        'yaml': 'pyyaml',
        'loguru': 'loguru',
    }
    
    missing = []
    success = []
    
    print("🔍 Checking Python packages...\n")
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✅ {package}")
            success.append(package)
        except ImportError:
            print(f"❌ {package} - NOT FOUND")
            missing.append(package)
    
    print(f"\n📊 Results: {len(success)}/{len(required_packages)} packages found")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"\nInstall missing packages with:")
        print(f"pip install {' '.join(missing)}")
        return False
    else:
        print("\n✅ All required packages are installed!")
        return True

def check_directories():
    """Check if essential directories exist."""
    import os
    
    essential_dirs = [
        'data/samples',
        'models',
        'logs',
        'src/ingest',
        'src/vision/detectors',
        'src/vision/tracking',
        'src/ui',
        'src/events',
        'src/llm',
        'src/pipeline',
    ]
    
    print("\n📁 Checking directories...\n")
    
    all_exist = True
    for directory in essential_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory} - NOT FOUND")
            all_exist = False
    
    return all_exist

def check_sample_video():
    """Check if sample video exists."""
    import os
    
    print("\n🎥 Checking sample video...\n")
    
    video_path = 'data/samples/sample.mp4'
    if os.path.exists(video_path):
        print(f"✅ Sample video found at {video_path}")
        return True
    else:
        print(f"⚠️  No sample video found at {video_path}")
        print(f"   See data/samples/README.md for instructions")
        return False

def main():
    """Run all checks."""
    print("=" * 60)
    print("Cricket AI - Environment Verification")
    print("=" * 60)
    print()
    
    packages_ok = check_imports()
    dirs_ok = check_directories()
    video_ok = check_sample_video()
    
    print("\n" + "=" * 60)
    
    if packages_ok and dirs_ok:
        print("✅ Environment is ready!")
        if not video_ok:
            print("⚠️  Add a sample video to test the pipeline")
        print("\nRun the test pipeline with:")
        print("  python src/pipeline/realtime_pipeline.py")
    else:
        print("❌ Environment setup incomplete")
        print("   Fix the issues above and run this script again")
        sys.exit(1)
    
    print("=" * 60)

if __name__ == "__main__":
    main()
