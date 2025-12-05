from ultralytics import YOLO
import torch

print("torch cuda:", torch.cuda.is_available())
print("device:", torch.cuda.get_device_name(0))

model = YOLO("yolov8n.pt").to("cuda")
print("model is on:", next(model.model.parameters()).device)
