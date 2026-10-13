@echo off
title PuzzleCam Setup

echo ==========================================
echo              PuzzleCam Setup
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1

if errorlevel 1 (
    echo [ERROR] Python was not found.
    echo.
    echo Please install Python 3.11 first.
    echo Make sure "Add Python to PATH" is selected.
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv

    if errorlevel 1 (
        echo.
        echo [ERROR] Could not create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

echo.

REM Upgrade pip
echo Updating pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo [ERROR] Could not update pip.
    pause
    exit /b 1
)

echo.

REM Install packages
echo Installing PuzzleCam dependencies...
echo This may take several minutes.
echo.

".venv\Scripts\python.exe" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ==========================================
    echo INSTALLATION FAILED
    echo ==========================================
    echo.
    echo Check your internet connection and the
    echo error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo          INSTALLATION COMPLETE!
echo ==========================================
echo.
echo PuzzleCam is ready.
echo.
echo Double-click run.bat to start the game.
echo.

pause