@echo off
echo Running Auto Clicker Demo Test...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python first.
    pause
    exit /b 1
)

echo Running demo test...
python demo_test.py

echo.
echo Demo test completed!
echo If all images are readable, you can run the main application with:
echo python run.py
echo.
pause
