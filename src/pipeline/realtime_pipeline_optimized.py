# src/pipeline/realtime_pipeline_optimized.py
import sys
from pathlib import Path
import time
import cv2
import threading
import queue
import numpy as np
import torch

# allow imports from project root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ingest.video_reader import VideoReader
from ui.overlay import draw_boxes
from vision.detectors.yolov8_detector import YoloV8Detector

# Config
VIDEO_PATH = Path("C:\\cricket-ai\\data\\samples\\test.mp4").resolve()
TARGET_WIDTH = 640   # try 640 for faster
TARGET_HEIGHT = 480
FRAME_SKIP = 1 # detect every FRAME_SKIP+1 frames (0 -> every frame)
DETECT_CONF = 0.35
MODEL_PATH = "yolov8n.pt"  # nano model
USE_AUTOMIXED = True  # use torch.amp.autocast on CUDA

# Thread-safe queues
frame_q = queue.Queue(maxsize=4)
result_q = queue.Queue(maxsize=4)
stop_event = threading.Event()

def reader_thread_fn(path, frame_q, stop_event):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        print("Reader: cannot open video", path)
        stop_event.set()
        return
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        # resize early to reduce bandwidth
        frame_small = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT), interpolation=cv2.INTER_LINEAR)
        try:
            frame_q.put_nowait((frame, frame_small))
        except queue.Full:
            # drop if queue full
            pass
    cap.release()
    stop_event.set()

def inference_thread_fn(frame_q, result_q, stop_event):
    # init detector on this thread (ensures device placement consistent)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print("Detector device:", device)
    detector = YoloV8Detector(model_path=MODEL_PATH, device=device)

    # Debug print to confirm model parameters device
    try:
        param_dev = next(detector.model.model.parameters()).device
        print("Internal model param device:", param_dev)
    except Exception as e:
        print("Could not read model parameter device:", e)

    frame_idx = 0
    while not stop_event.is_set():
        try:
            orig_frame, small_frame = frame_q.get(timeout=0.5)
        except queue.Empty:
            continue

        if (frame_idx % (FRAME_SKIP + 1)) == 0:
            t0 = time.time()
            # Use autocast for mixed precision on CUDA (recommended API)
            if device.startswith("cuda") and USE_AUTOMIXED:
                try:
                    with torch.amp.autocast(device_type="cuda", dtype=torch.float16):
                        dets = detector.predict(small_frame, conf=DETECT_CONF)
                except Exception as e:
                    print("autocast inference failed, falling back to full precision:", e)
                    dets = detector.predict(small_frame, conf=DETECT_CONF)
            else:
                dets = detector.predict(small_frame, conf=DETECT_CONF)
            infer_time = time.time() - t0
        else:
            dets = []  # skip detection this frame
            infer_time = 0.0

        try:
            result_q.put_nowait((orig_frame, small_frame, dets, infer_time))
        except queue.Full:
            pass
        frame_idx += 1

    stop_event.set()

def main():
    if not VIDEO_PATH.exists():
        print("Video missing:", VIDEO_PATH)
        return

    # start threads
    reader = threading.Thread(target=reader_thread_fn, args=(VIDEO_PATH, frame_q, stop_event), daemon=True)
    reader.start()

    inferer = threading.Thread(target=inference_thread_fn, args=(frame_q, result_q, stop_event), daemon=True)
    inferer.start()

    frame_count = 0
    total_infer_time = 0.0
    total_infer_calls = 0
    tstart = time.time()

    try:
        while not stop_event.is_set():
            try:
                orig_frame, small_frame, dets, infer_time = result_q.get(timeout=1.0)
            except queue.Empty:
                if stop_event.is_set():
                    break
                continue

            frame_count += 1
            if infer_time > 0:
                total_infer_time += infer_time
                total_infer_calls += 1

            # map detection boxes from small_frame coords to orig_frame coords
            h_orig, w_orig = orig_frame.shape[:2]
            h_small, w_small = small_frame.shape[:2]
            scale_x = w_orig / float(w_small)
            scale_y = h_orig / float(h_small)

            scaled_boxes = []
            for d in dets:
                x1, y1, x2, y2 = d['box']
                x1 = int(x1 * scale_x); x2 = int(x2 * scale_x)
                y1 = int(y1 * scale_y); y2 = int(y2 * scale_y)
                scaled_boxes.append((x1, y1, x2, y2, d['score'], d['name']))

            # draw boxes on original frame
            for (x1,y1,x2,y2,score,name) in scaled_boxes:
                cv2.rectangle(orig_frame, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(orig_frame, f"{name}:{score:.2f}", (x1, max(15,y1-5)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

            # compute simple FPS
            elapsed = time.time() - tstart
            fps = frame_count / elapsed if elapsed>0 else 0.0
            avg_infer = (total_infer_time / total_infer_calls) if total_infer_calls>0 else 0.0
            cv2.putText(orig_frame, f"FPS: {fps:.1f} AvgInfer: {avg_infer*1000:.1f}ms", (10,20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 1)

            cv2.imshow("Optimized Cricket AI", orig_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_event.set()
                break

    except KeyboardInterrupt:
        stop_event.set()

    reader.join(timeout=1.0)
    inferer.join(timeout=1.0)
    cv2.destroyAllWindows()
    print("Done. Frames:", frame_count)

if __name__ == "__main__":
    main()
