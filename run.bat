@echo off
title PuzzleCam

if not exist ".venv\Scripts\python.exe" (
    echo ==========================================
    echo PuzzleCam is not set up yet.
    echo ==========================================
    echo.
    echo Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

if not exist "models\hand_landmarker.task" (
    echo ==========================================
    echo Hand tracking model not found.
    echo ==========================================
    echo.
    echo Missing:
    echo models\hand_landmarker.task
    echo.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" main.py

if errorlevel 1 (
    echo.
    echo ==========================================
    echo PuzzleCam stopped with an error.
    echo ==========================================
    echo.
    pause
)