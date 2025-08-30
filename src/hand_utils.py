
from typing import List, Tuple
import cv2
import numpy as np

def draw_landmarks_and_box(image, landmarks_px: List[Tuple[int,int]], label: str = "", color=(0,255,0)):
    h, w = image.shape[:2]
    # Draw points
    for (x,y) in landmarks_px:
        cv2.circle(image, (int(x), int(y)), 3, color, -1)

    # Bounding box
    xs = [p[0] for p in landmarks_px]
    ys = [p[1] for p in landmarks_px]
    x1, y1, x2, y2 = int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    # Label
    if label:
        cv2.rectangle(image, (x1, y1 - 25), (x1 + 180, y1), color, -1)
        cv2.putText(image, label, (x1 + 6, y1 - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

    return (x1, y1, x2, y2)

def put_fps(image, fps: float):
    cv2.putText(image, f"FPS: {fps:.1f}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
