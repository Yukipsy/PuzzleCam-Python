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

- **Python 3.11** (Python 3.11.9 is supported)
- **Git**
- **Visual Studio Code**
- A webcam
- Windows 10/11 recommended

> **Important:** When installing Python, make sure **"Add Python to PATH"** is selected.

You do **not** need to manually install OpenCV, MediaPipe, Pygame, or NumPy. PuzzleCam's setup script will install the required Python packages automatically.

---

## 🚀 Quick Start with VS Code

### 1. Open VS Code

Open **Visual Studio Code**.

From the top menu, select:

```text
Terminal → New Terminal
```

A terminal will appear at the bottom of VS Code.

---

### 2. Clone PuzzleCam

In the VS Code terminal, run:

```powershell
git clone https://github.com/Yukipsy/PuzzleCam-Python.git
```

Wait for Git to finish downloading the project.

Then enter the project folder:

```powershell
cd PuzzleCam-Python
```

Your terminal should now end with something similar to:

```text
PS C:\Users\YourName\PuzzleCam-Python>
```

---

### 3. Open the PuzzleCam Folder in VS Code

In VS Code, select:

```text
File → Open Folder...
```

Select the newly cloned:

```text
PuzzleCam-Python
```

folder.

If VS Code asks whether you trust the authors of the files in this folder, choose the appropriate option for your workshop repository.

Then open a new terminal:

```text
Terminal → New Terminal
```

Make sure the terminal path ends with:

```text
\PuzzleCam-Python>
```

---

### 4. Set Up PuzzleCam

You only need to do this **once** after cloning the project.

In the VS Code terminal, run:

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

---

### 5. Run PuzzleCam

In the VS Code terminal, run:

```powershell
.\run.bat
```

PuzzleCam should now open. 🎉

---

## 🔁 Running It Again Later

You do **not** need to run `setup.bat` every time.

Open the `PuzzleCam-Python` folder in VS Code, open the terminal, and run:

```powershell
.\run.bat
```

That's all!

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

The completed photo will shatter and PuzzleCam will automatically restart.

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

### OpenCV

- Reads frames from the webcam
- Processes captured images
- Creates the black-and-white photo effect

### MediaPipe

- Detects hands
- Tracks hand landmarks
- Locates fingertips
- Detects pinch and fist gestures

### Pygame

- Displays the game interface
- Handles animations
- Handles mouse and keyboard input
- Plays sound effects

### NumPy

- Performs image and numerical operations

The project is divided into separate Python modules so you can explore how **computer vision, gesture recognition, image processing, and game logic** work together.

---

## 📦 Main Dependencies

```text
mediapipe
numpy
opencv-contrib-python
pygame
```

These are installed automatically when you run:

```powershell
.\setup.bat
```

---

## 💡 Workshop Learning

PuzzleCam is designed as an interactive Python workshop project for students learning how Python can be used beyond simple console programs.

By exploring the project, you can learn about:

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

Then restart VS Code and try again.

### `git` is not recognized

Git may not be installed or may not have been added to PATH.

Install Git, restart VS Code, and open a new terminal.

### Camera does not open

Close other programs that may be using your webcam, such as:

- Camera
- Zoom
- Microsoft Teams
- Discord
- OBS

Then run PuzzleCam again.

### `hand_landmarker.task` not found

Make sure this file exists:

```text
models/hand_landmarker.task
```

### Python packages are missing

Run:

```powershell
.\setup.bat
```

again.

### No sound

Make sure these files exist:

```text
assets/sounds/
├── countdown.wav
├── shutter.wav
├── correct.wav
├── wrong.wav
└── shatter.wav
```

---

## 🧩 Have Fun!

Experiment with the code, change the effects, modify the gestures, or add your own features.

PuzzleCam is a small example of what you can build when **Python meets computer vision and interaction**. 🚀