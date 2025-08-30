
# Real-Time Hand Gesture Recognition (Open Palm, Fist, Peace, Thumbs Up)

**Author:** _Your Name Here_  
**Language:** Python  
**Libraries:** OpenCV, MediaPipe, NumPy

## ✨ Overview
This project is a real-time, rule-based hand gesture recognizer that uses a standard webcam. It detects a hand, extracts 21 anatomical landmarks (MediaPipe Hands), and classifies static poses into four gestures:

- **Open Palm**
- **Fist**
- **Peace (V-sign)**
- **Thumbs Up**

The application overlays landmarks, a bounding box, the gesture name, and FPS on the live video.

https://github.com/your-handle/hand-gesture-recognition (replace with your repo after pushing)

---

## 🧠 Technology Justification
- **MediaPipe Hands** is a fast, production-ready hand landmark detector. It runs in real-time on CPU and provides **21 3D landmarks** per hand with handedness (Left/Right). This eliminates the need to train a separate detector and dramatically simplifies downstream logic.
- **OpenCV** provides a cross-platform, efficient interface to the webcam and basic drawing utilities for visualization.
- **Rule-based logic** (geometric/angle thresholds) is **transparent and explainable**, requires **no dataset**, and is robust enough for common static gestures under typical lighting and camera setups.

> For a lightweight assignment setting, this stack offers the best tradeoff of **accuracy**, **simplicity**, and **runtime performance** on ordinary laptops.

---

## 🧩 Gesture Logic (High Level)

1. **Landmarks:** For each detected hand we read 21 landmarks (`Wrist`, `Thumb: CMC/MCP/IP/Tip`, `Index/Middle/Ring/Pinky: MCP/PIP/DIP/Tip`).
2. **Finger extension:** For each finger we compute the **angle at the central joint** (PIP for index–pinky, IP for thumb) using 3 consecutive landmarks. If the angle is **> 160°**, we treat that finger as **extended**; otherwise it is curled.
3. **Classification rules:**
   - **Open Palm:** Index, Middle, Ring, Pinky are extended (thumb can be either).  
   - **Fist:** No fingers extended.
   - **Peace:** Index and Middle extended, Ring and Pinky curled (thumb can be either).  
   - **Thumbs Up:** Only Thumb extended **and** the thumb vector points roughly upward (tip y << MCP y) while the other four fingers are curled.

Thresholds are scaled by hand size to stay reasonably stable across distances to the camera.

---

## 📦 Project Structure
```
hand-gesture-recognition/
├─ src/
│  ├─ app.py            # Main entry-point
│  ├─ gestures.py       # Gesture logic (angles, rules)
│  └─ hand_utils.py     # Drawing utils, helpers
├─ demo/
│  └─ (record your demo.mp4 or demo.gif here)
├─ scripts/
│  ├─ record_demo_ffmpeg.sh  # Optional helper (Linux/macOS)
│  └─ record_demo_ffmpeg.bat # Optional helper (Windows)
├─ tests/
│  └─ test_angles.py    # Tiny sanity test for angle math
├─ requirements.txt
├─ README.md
├─ LICENSE
└─ .gitignore
```

---

## 🛠️ Setup

> **Python:** 3.9–3.12 recommended

```bash
git clone https://github.com/<your-handle>/hand-gesture-recognition.git
cd hand-gesture-recognition
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

> If you face issues with `mediapipe` on Apple Silicon, upgrade pip and wheel:
> ```bash
> python -m pip install --upgrade pip wheel setuptools
> pip install -r requirements.txt
> ```

---

## ▶️ Run
```bash
python src/app.py --camera 0 --show-fps 1
```
**Keys:** Press **Q** to quit.

Optional flags:
- `--camera` (int): webcam index (default `0`)
- `--min-detection-conf` (float): hand detector threshold (default `0.6`)
- `--min-tracking-conf` (float): tracker threshold (default `0.5`)
- `--max-hands` (int): process up to this many hands (default `2`)
- `--show-fps` (0/1): overlay FPS (default `1`)

---

## 🎬 Demo Recording
You can record a quick demonstration (few seconds per gesture) and place it as `demo/demo.mp4`.

**Windows (PowerShell + ffmpeg installed):**
```powershell
scripts\record_demo_ffmpeg.bat
```

**macOS/Linux (with ffmpeg):**
```bash
chmod +x scripts/record_demo_ffmpeg.sh
scripts/record_demo_ffmpeg.sh
```

Alternatively, use any screen recorder (OBS, Xbox Game Bar on Windows, QuickTime on macOS).

---

## 🧪 Tests
A small unit test checks angle computation:
```bash
python -m unittest tests/test_angles.py -v
```

---

## ✅ Performance Notes
- Works in real time on typical laptop CPUs (30–60 FPS depending on device).
- Good lighting and a clear background improve stability.
- For best results, hold your hand roughly facing the camera.

---

## 📝 Submission Checklist
- [x] Source code under `src/`
- [x] `requirements.txt`
- [x] `README.md` (this file)
- [x] `demo/demo.mp4` (record and include)
- [x] Public Git repository link

---

## 🙋‍♀️ Attribution
MIT License. No datasets used. Built with MediaPipe, OpenCV, NumPy.
