# src/vision/detectors/yolov8_detector.py
from ultralytics import YOLO
import time

class YoloV8Detector:
    def __init__(self, model_path='yolov8n.pt', device=None):
        """
        model_path: path to .pt file, or model name 'yolov8n.pt'
        device: 'cpu' or 'cuda:0' (None -> auto)
        """
        self.model = YOLO(model_path)
        if device:
            self.model.to(device)
        # warm-up once
        self.warmed = False

    def predict(self, frame, conf=0.25, iou=0.45, verbose=False):
        """
        Run model on BGR OpenCV frame.
        Returns list of detections: [{'box':[x1,y1,x2,y2], 'score':float, 'class':int, 'name':str}, ...]
        """
        # Ultralytics accepts numpy BGR frames directly
        if not self.warmed:
            # tiny warmup using a single inference
            _ = self.model(frame, conf=conf, iou=iou, verbose=False)
            self.warmed = True

        results = self.model(frame, conf=conf, iou=iou, verbose=False)
        detections = []
        # results is a list (per batch) — we pass single image so use results[0]
        r = results[0]
        boxes = r.boxes  # Boxes object
        for box in boxes:
            xyxy = box.xyxy.cpu().numpy().tolist()[0]  # [x1,y1,x2,y2]
            score = float(box.conf.cpu().numpy().tolist()[0])
            cls = int(box.cls.cpu().numpy().tolist()[0])
            name = self.model.names.get(cls, str(cls))
            detections.append({'box': xyxy, 'score': score, 'class': cls, 'name': name})
        return detections
