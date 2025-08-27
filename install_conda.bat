@echo off
echo Auto Clicker - Cai dat voi Conda/Miniconda
echo ==========================================
echo.

REM Check if conda is installed
conda --version >nul 2>&1
if errorlevel 1 (
    echo Conda khong duoc tim thay!
    echo Neu ban co Anaconda/Miniconda, hay mo Anaconda Prompt
    echo Neu chua co, download tai: https://docs.conda.io/en/latest/miniconda.html
    echo.
    echo Sau khi cai dat conda, chay file nay trong Anaconda Prompt
    pause
    exit /b 1
)

echo Conda da duoc tim thay, dang cai dat...
echo.

REM Create conda environment (optional)
echo Tao moi truong conda moi? (y/n)
set /p create_env="Nhap y de tao moi truong moi, n de dung moi truong hien tai: "

if /i "%create_env%"=="y" (
    echo Tao moi truong conda 'auto-clicker'...
    conda create -n auto-clicker python=3.9 -y
    conda activate auto-clicker
)

REM Install packages with conda
echo.
echo Cai dat cac thu vien...
conda install -c conda-forge numpy opencv pillow -y
pip install pyautogui

echo.
echo ===========================================
echo Cai dat hoan thanh!
echo.
echo Kiem tra cai dat:
python -c "import cv2, pyautogui, numpy, PIL; print('Tat ca thu vien da duoc cai dat thanh cong!')"

if errorlevel 1 (
    echo Co loi xay ra! Kiem tra lai cai dat.
) else (
    echo Cai dat thanh cong!
    if /i "%create_env%"=="y" (
        echo.
        echo Luu y: Ban da tao moi truong 'auto-clicker'
        echo De kich hoat moi truong nay: conda activate auto-clicker
        echo Sau do chay: python run.py
    ) else (
        echo Ban co the chay ung dung: python run.py
    )
)

echo.
pause
