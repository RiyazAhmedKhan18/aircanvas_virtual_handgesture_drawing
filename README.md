# AirCanvas — Virtual Hand Gesture Drawing

Draw in the air using just your hand and a webcam! AirCanvas uses **MediaPipe** for real-time hand landmark detection and **OpenCV** to track your index finger and paint strokes on a virtual canvas — no mouse, no touch, no stylus needed.

---

## Demo

Two windows open when you run the app:
- **Output** — Live webcam feed with hand landmarks and the UI toolbar
- **Paint** — Clean white canvas showing only your drawing

---

##  Features

-  Real-time hand tracking using MediaPipe
-  Draw in 4 colors — Blue, Green, Red, Yellow
-  Pinch gesture to lift the pen (stop drawing)
-  CLEAR button to wipe the canvas
-  QUIT button to exit the app
-  Separate clean paint window with no UI clutter

---

## Tech Stack

- Python 3.x
- OpenCV (`cv2`)
- MediaPipe
- NumPy

---

##  Installation

**1. Clone the repository:**
```bash
git clone https://github.com/RiyazAhmedKhan18/aircanvas_virtual_handgesture_drawing.git
cd aircanvas_virtual_handgesture_drawing
```

**2. Create and activate a virtual environment (recommended):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install opencv-python mediapipe numpy
```

---

## ▶️ Usage

```bash
python air_canvas.py
```

Make sure your webcam is connected. Allow camera access if prompted.

---

## 🖌️ How to Use

| Gesture / Action | Result |
|---|---|
| Point index finger | Draw on canvas |
| Bring thumb close to index finger | Lift pen (stop drawing) |
| Move finger to **BLUE** button | Switch to blue |
| Move finger to **GREEN** button | Switch to green |
| Move finger to **RED** button | Switch to red |
| Move finger to **YELLOW** button | Switch to yellow |
| Move finger to **CLEAR** button | Wipe the canvas |
| Move finger to **QUIT** button | Exit the app |
| Press `q` on keyboard | Exit the app |

> All buttons are located at the **top of the webcam window**.

---

## 📁 Project Structure

```
aircanvas_virtual_handgesture_drawing/
│
├── air_canvas.py       # Main application script
├── README.md           # Project documentation
└── .gitignore          # Excludes venv and cache files
```

---

##  Requirements

- Python 3.7+
- Webcam
- Good lighting for accurate hand detection

---

##  Author
**Riyaz Ahmed Khan**  
B.E. CSE (AI/ML) — MITE Mangalore  
[GitHub](https://github.com/RiyazAhmedKhan18)

**Riyaz Ahmed Khan**  
B.E. CSE (AI/ML) — MITE Mangalore  
[GitHub](https://github.com/RiyazAhmedKhan18)
