@echo off
echo Installing Auto Clicker dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python first.
    pause
    exit /b 1
)

echo Python found, installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error installing dependencies!
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo You can now run the application with: python run.py
echo.
pause
