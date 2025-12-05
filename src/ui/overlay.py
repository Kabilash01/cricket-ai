import cv2

def draw_boxes(frame, boxes, color=(0,255,0)):
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
    return frame
