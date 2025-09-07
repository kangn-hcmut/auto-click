@echo off
echo ========================================
echo Cài đặt PyInstaller - Khắc phục lỗi
echo ========================================
echo.

echo 🔧 Thử cài đặt PyInstaller với nhiều phương pháp...
echo.

echo 📋 Phương pháp 1: Cài đặt thông thường
pip install pyinstaller
echo.

echo 📋 Phương pháp 2: Cài đặt với quyền user
pip install --user pyinstaller
echo.

echo 📋 Phương pháp 3: Cài đặt với cache mới  
pip install --no-cache-dir pyinstaller
echo.

echo 📋 Phương pháp 4: Sử dụng python -m pip
python -m pip install pyinstaller
echo.

echo 📋 Phương pháp 5: Force reinstall
pip uninstall pyinstaller -y
pip install pyinstaller --force-reinstall --no-cache-dir
echo.

echo 🔍 Kiểm tra cài đặt...
pyinstaller --version
if %ERRORLEVEL% EQU 0 (
    echo ✅ PyInstaller đã cài đặt thành công!
    echo 🚀 Có thể chạy build_exe.bat hoặc build_exe_fix.bat
) else (
    echo ❌ Vẫn gặp lỗi! Thử các giải pháp sau:
    echo.
    echo 💡 Giải pháp 1: Chạy Command Prompt với quyền Administrator
    echo    - Nhấn Win + X, chọn "Windows PowerShell (Admin)"
    echo    - Chạy lại script này
    echo.
    echo 💡 Giải pháp 2: Cài đặt Anaconda
    echo    - Download từ anaconda.com
    echo    - Sau khi cài: conda install pyinstaller
    echo.
    echo 💡 Giải pháp 3: Cài đặt Python mới
    echo    - Download Python từ python.org
    echo    - Chọn "Add to PATH" khi cài đặt
    echo.
    echo 💡 Giải pháp 4: Sử dụng virtual environment
    echo    - python -m venv venv
    echo    - venv\Scripts\activate
    echo    - pip install pyinstaller
)

echo.
pause
