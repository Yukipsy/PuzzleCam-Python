# PuzzleCam 🧩📸

PuzzleCam is an interactive photo puzzle built with Python, OpenCV,
MediaPipe and Pygame.

Use your hands to frame a photo, pinch to capture it, and solve the
shuffled 3×3 puzzle using hand gestures or your mouse.

Once all 9 pieces are solved, make a fist to shatter the completed
photo and start again!

## ✨ Features

- Real-time webcam display
- MediaPipe hand tracking
- Two-hand photo framing
- Pinch-to-capture gesture
- Animated 3-2-1 countdown
- Black-and-white photo effect
- 3×3 photo puzzle
- Pinch-and-drag puzzle control
- Mouse drag support
- Correct and wrong placement feedback
- Fist gesture detection
- Shatter animation
- Automatic restart

## 🛠 Requirements

You need:

- Python 3.11
- A webcam
- Git
- Windows 10/11 recommended

## 🚀 Quick Start

### 1. Clone this repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Then enter the project folder:

```bash
cd PuzzleCam-Python
```

### 2. Setup

On Windows, double-click:

```text
setup.bat
```

This will automatically:

1. Check Python
2. Create a virtual environment
3. Install the required Python packages

The first installation may take several minutes.

### 3. Run PuzzleCam

Double-click:

```text
run.bat
```

That's it!

## 🎮 How to Play

### Step 1 — Frame

Hold up two hands.

Your two index fingers define the photo frame.

### Step 2 — Capture

Pinch both hands and hold.

PuzzleCam will count down:

```text
3 → 2 → 1
```

The captured area becomes a black-and-white photo.

### Step 3 — Remember

Remember the original image before the puzzle is shuffled!

### Step 4 — Solve

You can use either hand gestures or a mouse.

#### Hand Control

```text
Pinch → Move → Release
```

Pinch a puzzle piece, move your hand, and release it over the correct
position.

#### Mouse Control

```text
Click → Drag → Release
```

Left-click a puzzle piece, drag it, and release it over the correct
position.

Correct pieces are locked into place.

### Step 5 — Finish

Complete all:

```text
9 / 9
```

Then make a fist and hold it.

The completed photo will shatter and PuzzleCam automatically restarts.

## ⌨️ Keyboard Controls

| Key | Action |
|---|---|
| `R` | Restart |
| `Q` | Quit |

## 📁 Project Structure

```text
PuzzleCam-Python/
├── main.py
├── requirements.txt
├── setup.bat
├── run.bat
├── models/
│   └── hand_landmarker.task
└── src/
    ├── __init__.py
    ├── animations.py
    ├── camera.py
    ├── hand_tracker.py
    ├── puzzle.py
    └── ui.py
```

## 🧠 How It Works

PuzzleCam combines several Python concepts:

**OpenCV**
- Reads frames from the webcam
- Processes captured images

**MediaPipe**
- Detects hands
- Tracks hand landmarks
- Detects pinch and fist gestures

**Pygame**
- Displays the game interface
- Handles animations
- Handles mouse input

**NumPy**
- Performs image and numerical operations

The project is divided into separate Python modules so students can
explore how computer vision, gesture recognition and game logic work
together.

## 📦 Main Dependencies

```text
mediapipe
numpy
opencv-contrib-python
pygame
```

## 💡 Workshop

This project is designed as an interactive Python workshop project for
students learning how Python can be used beyond console programs.

Topics demonstrated include:

- Python modules
- Classes and objects
- Computer vision
- Hand landmark tracking
- Gesture recognition
- Image processing
- Game loops
- State machines
- User interaction
- Animation

## 📸 Camera Permission

If PuzzleCam cannot access your webcam, make sure Windows allows desktop
applications to use the camera:

**Settings → Privacy & security → Camera → Let desktop apps access your camera**

## ⚠️ Troubleshooting

### Camera does not open

Close other programs that may be using the webcam, such as Zoom, Teams
or another camera application.

### `hand_landmarker.task` not found

Make sure this file exists:

```text
models/hand_landmarker.task
```

### Packages are missing

Run:

```text
setup.bat
```

again.

### Restart PuzzleCam

Press:

```text
R
```

### Quit PuzzleCam

Press:

```text
Q
```