# Virtual Mouse using Hand Gestures

A Python-based virtual mouse that uses your webcam and hand gestures to control the cursor, perform clicks, and navigate the screen. Built using **OpenCV**, **MediaPipe**, and **PyAutoGUI**.

---

## Features / Hand Gestures

| Gesture | Action |
|---------|--------|
| **Index + Thumb pinch** | Left Click |
| **Middle + Thumb pinch** | Right Click |
| **Ring + Thumb pinch** | Scroll / Press Down Arrow |
| **Pinky + Thumb pinch** | Scroll / Press Up Arrow |
| **Move Index Finger** | Move Cursor on Screen |

> Smooth cursor movement is implemented for better control.  

---

## Requirements

- Python 3.8+
- Webcam
- Packages:
  ```bash
  pip install opencv-python mediapipe pyautogui
