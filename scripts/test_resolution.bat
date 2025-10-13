@echo off
echo ========================================
echo     Auto Clicker - Resolution Test
echo ========================================
echo.

echo Testing image detection on different screen resolutions...
echo.

cd /d "%~dp0\.."

echo Testing all images...
python scripts\test_resolution.py

echo.
echo ========================================
echo Test specific image (example):
echo   python scripts\test_resolution.py ads.png 0.7
echo   python scripts\test_resolution.py Gems.png 0.8
echo ========================================

pause