@echo off
echo Auto Clicker - Cai dat thu vien (Fix loi)
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python khong duoc tim thay! Vui long cai dat Python truoc.
    echo Download tai: https://python.org
    pause
    exit /b 1
)

echo Python da duoc cai dat, dang cai dat thu vien...
echo.

REM Upgrade pip first
echo Buoc 1: Cap nhat pip...
python -m pip install --upgrade pip

REM Install numpy first (pre-compiled wheel)
echo.
echo Buoc 2: Cai dat numpy...
python -m pip install numpy --only-binary=all

if errorlevel 1 (
    echo Loi khi cai dat numpy! Thu cach khac...
    echo Cai dat numpy tu conda-forge...
    python -m pip install --index-url https://pypi.anaconda.org/conda-forge/simple numpy
    
    if errorlevel 1 (
        echo Van gap loi! Vui long thu cai dat manual:
        echo pip install --only-binary=:all: numpy
        pause
        exit /b 1
    )
)

REM Install other packages
echo.
echo Buoc 3: Cai dat cac thu vien khac...
python -m pip install pyautogui Pillow

echo.
echo Buoc 4: Cai dat OpenCV...
python -m pip install opencv-python

if errorlevel 1 (
    echo Loi khi cai dat cac thu vien!
    echo Thu cai dat bang cach khac...
    python -m pip install --user pyautogui Pillow opencv-python
)

echo.
echo ===========================================
echo Cai dat hoan thanh!
echo.
echo Kiem tra cai dat:
python -c "import cv2, pyautogui, numpy, PIL; print('Tat ca thu vien da duoc cai dat thanh cong!')"

if errorlevel 1 (
    echo.
    echo Co loi xay ra! Vui long kiem tra lai.
    echo Hay thu chay: python demo_test.py
) else (
    echo.
    echo Cai dat thanh cong! Ban co the chay ung dung:
    echo python run.py
)

echo.
pause
