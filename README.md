Real-Time Hand Gesture Recognition (Open Palm, Fist, Peace, Thumbs Up)

Author: Karan Desai
Language: Python
Libraries: OpenCV, MediaPipe, NumPy

✨ Overview

This project implements a real-time hand gesture recognition system using a standard webcam. It detects a hand, extracts 21 anatomical landmarks using MediaPipe, and classifies static poses into four gestures:

Open Palm

Fist

Peace (V-sign)

Thumbs Up

The application overlays the detected landmarks, bounding box, gesture name, and FPS on the live video stream.

🧠 Technology Justification

MediaPipe Hands: Provides accurate and efficient hand landmark detection (21 3D points), enabling gesture recognition without training a separate model.

OpenCV: Handles video capture and visualization with minimal overhead.

Rule-Based Logic: Transparent and easy to implement for static gestures, requiring no training data while maintaining good performance for common poses.

🧩 Gesture Recognition Logic

Landmark Detection: Extract 21 hand landmarks.

Finger State Analysis: Determine if each finger is extended or curled using joint angles.

Classification Rules:

Open Palm: All four fingers extended (thumb optional).

Fist: All fingers curled.

Peace: Index and middle extended, others curled.

Thumbs Up: Thumb extended upward, others curled.

📦 Project Structure
hand-gesture-recognition/
├─ src/
│  ├─ app.py            # Main application
│  ├─ gestures.py       # Gesture classification logic
│  └─ hand_utils.py     # Drawing helpers
├─ requirements.txt
├─ README.md
└─ demo/
   └─ demo.mp4          # Short demonstration video

🛠️ Setup

Python: 3.9–3.12 recommended

git clone https://github.com/<your-handle>/hand-gesture-recognition.git
cd hand-gesture-recognition
python -m venv .venv
# Activate virtual environment:
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

▶️ Run the Application
python src/app.py --camera 0


Press Q to quit.

✅ Performance Notes

Works in real time on most laptops (30–60 FPS).

For best results: good lighting and a clear background.

📜 License

MIT License.
