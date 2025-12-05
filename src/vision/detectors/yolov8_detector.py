from ultralytics import YOLO
import torch

class YoloV8Detector:
    def __init__(self, model_path='yolov8n.pt', device=None):
        self.device = device or ("cuda:0" if torch.cuda.is_available() else "cpu")
        print("[YOLO] Loading model on device:", self.device)

        self.model = YOLO(model_path)

        # FORCE device
        try:
            self.model.to(self.device)
        except Exception as e:
            print("WARNING: .to(device) failed:", e)

        self.warmed = False

    def predict(self, frame, conf=0.25, iou=0.45, verbose=False):
        # Force device EACH CALL (YOLO sometimes ignores internal device)
        if hasattr(self.model, "predictor") and hasattr(self.model.predictor, "model"):
            try:
                self.model.predictor.model.to(self.device)
            except:
                pass

        # Run inference
        results = self.model(frame, device=self.device, conf=conf, iou=iou, verbose=False)

        detections = []
        r = results[0]
        for b in r.boxes:
            xyxy = b.xyxy.cpu().numpy().tolist()[0]
            score = float(b.conf.cpu().numpy().tolist()[0])
            cls = int(b.cls.cpu().numpy().tolist()[0])
            name = self.model.names.get(cls, str(cls))
            detections.append({'box': xyxy, 'score': score, 'class': cls, 'name': name})
        return detections
