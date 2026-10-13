# PuzzleCam 🧩📸

PuzzleCam is an interactive photo puzzle built with **Python, OpenCV, MediaPipe, Pygame, and NumPy**.

Use your hands to frame a photo, pinch to capture it, and solve the shuffled **3×3 puzzle** using hand gestures or your mouse.

Once all 9 pieces are solved, make a fist to shatter the completed photo and start again!

---

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
- Sound effects
- Fist gesture detection
- Shatter animation
- Automatic restart

---

## 🛠 Before You Start

Make sure your computer has:

- **Python 3.11**
- **Git**
- A webcam
- Windows 10/11 recommended

> **Important:** When installing Python, make sure **"Add Python to PATH"** is selected.

You do **not** need to manually install OpenCV, MediaPipe, Pygame, or NumPy. The setup script will install the required Python packages for you.

---

## 🚀 Quick Start

### 1. Clone PuzzleCam

Open **PowerShell** and run:

```powershell
git clone https://github.com/Yukipsy/PuzzleCam-Python.git
cd PuzzleCam-Python
```

### 2. Set Up PuzzleCam

For the **first time only**, run:

```powershell
.\setup.bat
```

The setup script will automatically:

1. Check that Python is available
2. Create a virtual environment (`.venv`)
3. Update `pip`
4. Install all required Python packages

The first installation may take several minutes.

Wait until you see:

```text
INSTALLATION COMPLETE!

PuzzleCam is ready.
```

### 3. Run PuzzleCam

Run:

```powershell
.\run.bat
```

That's it! 🎉

### Next Time

You do **not** need to run `setup.bat` again.

Open the PuzzleCam folder and simply run:

```powershell
.\run.bat
```

You can also double-click `run.bat` from File Explorer.

---

## 🎮 How to Play

### Step 1 — Frame

Hold up **two hands** in front of the webcam.

Your two index fingers define the photo frame.

Try to keep your hands far enough apart to create a large enough photo.

### Step 2 — Capture

Pinch with **both hands** and hold.

PuzzleCam will count down:

```text
3 → 2 → 1
```

The selected area will be captured and transformed into a black-and-white photo.

### Step 3 — Remember

Remember the original image before the puzzle is shuffled!

### Step 4 — Solve

The photo becomes a shuffled **3×3 puzzle**.

You can solve it using either hand gestures or your mouse.

#### Hand Control

```text
Pinch → Move → Release
```

Pinch a puzzle piece, move your hand, and release it over the position where you think it belongs.

#### Mouse Control

```text
Click → Drag → Release
```

Left-click a puzzle piece, drag it, and release it over the position where you think it belongs.

Correctly placed pieces are locked into position.

### Step 5 — Finish

Complete all:

```text
9 / 9
```

Then make a **fist and hold it**.

The completed photo will shatter and PuzzleCam will automatically restart for another round.

---

## ⌨️ Keyboard Controls

| Key | Action |
| --- | --- |
| `R` | Restart PuzzleCam |
| `Q` | Quit PuzzleCam |

---

## 📁 Project Structure

```text
PuzzleCam-Python/
├── main.py
├── README.md
├── requirements.txt
├── setup.bat
├── run.bat
├── .gitignore
│
├── assets/
│   └── sounds/
│       ├── countdown.wav
│       ├── shutter.wav
│       ├── correct.wav
│       ├── wrong.wav
│       └── shatter.wav
│
├── models/
│   └── hand_landmarker.task
│
└── src/
    ├── __init__.py
    ├── animations.py
    ├── camera.py
    ├── hand_tracker.py
    ├── puzzle.py
    ├── sound.py
    └── ui.py
```

---

## 🧠 How It Works

PuzzleCam combines several Python libraries and programming concepts.

### OpenCV

Used to:

- Read frames from the webcam
- Process captured images
- Create the black-and-white photo effect

### MediaPipe

Used to:

- Detect hands
- Track hand landmarks
- Locate fingertips
- Detect pinch gestures
- Detect fist gestures

### Pygame

Used to:

- Display the game interface
- Draw the puzzle and visual effects
- Handle animations
- Handle mouse and keyboard input
- Play sound effects

### NumPy

Used for image and numerical operations, including the photo effect.

The project is divided into separate Python modules so you can explore how **computer vision, gesture recognition, image processing, and game logic** work together.

---

## 📦 Main Dependencies

The main Python packages used are:

```text
mediapipe
numpy
opencv-contrib-python
pygame
```

They are installed automatically when you run:

```powershell
.\setup.bat
```

---

## 💡 Workshop Learning

PuzzleCam is designed as an interactive Python workshop project for students learning how Python can be used beyond simple console programs.

By exploring the code, you can learn about:

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
- Sound effects

Try modifying the code and see how the game changes!

---

## 📸 Camera Permission

If PuzzleCam cannot access your webcam, make sure Windows allows desktop applications to use the camera.

Go to:

```text
Settings
→ Privacy & security
→ Camera
→ Let desktop apps access your camera
```

Make sure camera access is enabled.

---

## ⚠️ Troubleshooting

### `python` is not recognized

Python may not be installed or may not have been added to your system PATH.

Install **Python 3.11** and make sure **"Add Python to PATH"** is selected during installation.

Then close and reopen PowerShell.

### `git` is not recognized

Install Git for Windows, then close and reopen PowerShell before trying the clone command again.

### Camera does not open

Close other applications that may already be using the webcam, such as:

- Camera
- Zoom
- Microsoft Teams
- Discord
- OBS

Then restart PuzzleCam.

### `hand_landmarker.task` not found

Make sure this file exists:

```text
models/hand_landmarker.task
```

If you cloned the complete repository, this file should already be included.

### Python packages are missing

Run the setup script again:

```powershell
.\setup.bat
```

### No sound

Make sure the sound files exist inside:

```text
assets/sounds/
```

The folder should contain:

```text
countdown.wav
shutter.wav
correct.wav
wrong.wav
shatter.wav
```

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

---

## 🧩 Have Fun!

Experiment with the code, change the effects, modify the gestures, or add your own features.

PuzzleCam is not just a game — it's a small example of what you can build when **Python meets computer vision and interaction**. 🚀