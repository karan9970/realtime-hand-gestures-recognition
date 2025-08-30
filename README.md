# Hand Gesture Recognition

A simple real-time hand gesture recognition system built with **OpenCV** and **MediaPipe**.  
The application detects hand landmarks and maps them to predefined gestures using Python.

## Features
- Real-time hand tracking using webcam
- Gesture classification logic (easily extendable)
- Lightweight and beginner-friendly

## Tech Stack
- [OpenCV](https://opencv.org/) – For video processing
- [MediaPipe](https://developers.google.com/mediapipe) – For hand landmark detection
- [NumPy](https://numpy.org/) – For data handling

## Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/karan9970/realtime-hand-gestures-recognition.git
cd hand-gesture-recognition
pip install -r requirements.txt
```

## Usage
Run the main application:

```bash
python src/app.py
```

Press **`q`** to exit the application.

## Example Output
- Displays hand landmarks on webcam feed
- Detects basic gestures like *Thumbs Up* and *Peace Sign* ,*Palm*
