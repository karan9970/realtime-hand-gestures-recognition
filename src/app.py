
import argparse
import time
from typing import Tuple
import cv2
import numpy as np
import mediapipe as mp

from gestures import classify_gesture
from hand_utils import draw_landmarks_and_box, put_fps

def normalized_to_pixel_coords(nx, ny, image_width, image_height):
    x_px = min(int(nx * image_width), image_width - 1)
    y_px = min(int(ny * image_height), image_height - 1)
    return x_px, y_px

def main():
    parser = argparse.ArgumentParser(description="Real-time Hand Gesture Recognition (OpenCV + MediaPipe)")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--min-detection-conf", type=float, default=0.6)
    parser.add_argument("--min-tracking-conf", type=float, default=0.5)
    parser.add_argument("--max-hands", type=int, default=2)
    parser.add_argument("--show-fps", type=int, default=1)
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam. Try --camera 1 or check permissions.")
        return

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        model_complexity=1,
        max_num_hands=args.max_hands,
        min_detection_confidence=args.min_detection_conf,
        min_tracking_confidence=args.min_tracking_conf,
    )
    mp_draw = mp.solutions.drawing_utils
    mp_styles = mp.solutions.drawing_styles

    last_time = time.time()
    fps = 0.0

    win_name = "Hand Gestures"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            # Do NOT flip horizontally to avoid confusing thumbs-up orientation.
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False
            result = hands.process(image_rgb)
            image_rgb.flags.writeable = True

            h, w = frame.shape[:2]

            if result.multi_hand_landmarks:
                for idx, lmset in enumerate(result.multi_hand_landmarks):
                    # Get handedness label if available
                    handedness = ""
                    if result.multi_handedness and len(result.multi_handedness) > idx:
                        handedness = result.multi_handedness[idx].classification[0].label

                    # Classify gesture
                    label, states = classify_gesture(lmset.landmark, handedness)

                    # Convert landmarks to pixel coords for drawing
                    pts_px = [normalized_to_pixel_coords(lm.x, lm.y, w, h) for lm in lmset.landmark]

                    # Draw skeleton for visual clarity
                    mp_draw.draw_landmarks(
                        frame,
                        lmset,
                        mp_hands.HAND_CONNECTIONS,
                        mp_styles.get_default_hand_landmarks_style(),
                        mp_styles.get_default_hand_connections_style(),
                    )

                    # Draw bounding box + label
                    status_str = f"{label} ({handedness})" if handedness else label
                    draw_landmarks_and_box(frame, pts_px, label=status_str, color=(0,255,0))

            # FPS calc
            if args.show_fps:
                now = time.time()
                dt = now - last_time
                if dt > 0:
                    fps = 0.9 * fps + 0.1 * (1.0 / dt) if fps > 0 else (1.0 / dt)
                last_time = now
                put_fps(frame, fps)

            cv2.imshow(win_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                break

    finally:
        hands.close()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
