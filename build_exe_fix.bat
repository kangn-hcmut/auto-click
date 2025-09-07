@echo off
echo ========================================
echo Auto Clicker - Build EXE Fix Script
echo ========================================
echo.

echo ⚠️  Phát hiện lỗi cài đặt PyInstaller!
echo 🔧 Đang thử các phương pháp khắc phục...
echo.

echo 📋 Phương pháp 1: Cài đặt với quyền user
pip install --user pyinstaller
echo.

echo 📋 Phương pháp 2: Cài đặt với cache mới
pip install --no-cache-dir pyinstaller
echo.

echo 📋 Phương pháp 3: Force reinstall
pip uninstall pyinstaller -y
pip install pyinstaller --force-reinstall
echo.

echo 📋 Phương pháp 4: Cài đặt từ conda (nếu có)
conda install pyinstaller -y 2>nul
echo.

echo 🔍 Kiểm tra PyInstaller đã cài đặt thành công...
pyinstaller --version
if %ERRORLEVEL% EQU 0 (
    echo ✅ PyInstaller đã sẵn sàng!
    echo.
    echo 🚀 Bắt đầu build ứng dụng...
    goto :build
) else (
    echo ❌ PyInstaller vẫn chưa hoạt động!
    echo.
    echo 💡 Thử các giải pháp sau:
    echo 1. Chạy Command Prompt với quyền Administrator
    echo 2. Sử dụng: python -m pip install pyinstaller
    echo 3. Cài đặt Python mới từ python.org
    echo 4. Sử dụng Anaconda thay vì Python thường
    echo.
    pause
    exit /b 1
)

:build
echo ========================================
echo 🔨 Đang build ứng dụng...
echo ========================================

python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "AutoClicker-GameBot" ^
    --add-data "image;image" ^
    --distpath "build/dist" ^
    --workpath "build/work" ^
    --specpath "build" ^
    --clean ^
    run.py

echo.
if exist "build\dist\AutoClicker-GameBot.exe" (
    echo ✅ Build thành công!
    echo 📁 File EXE: build\dist\AutoClicker-GameBot.exe
    echo 📋 Kích thước: 
    dir "build\dist\AutoClicker-GameBot.exe" | find "AutoClicker-GameBot.exe"
    echo.
    echo 📦 Tạo package đầy đủ...
    if not exist "build\dist\package" mkdir "build\dist\package"
    copy "build\dist\AutoClicker-GameBot.exe" "build\dist\package\"
    xcopy "image" "build\dist\package\image" /E /I /Y
    copy "readme.md" "build\dist\package\"
    
    echo ✅ Package hoàn thành: build\dist\package\
    echo.
    echo Mở thư mục package? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" explorer "build\dist\package"
) else (
    echo ❌ Build thất bại!
    echo 🔍 Kiểm tra lỗi và thử lại
    echo.
    echo 💡 Gợi ý:
    echo - Kiểm tra thư mục 'image' có đầy đủ file
    echo - Đảm bảo run.py và auto_clicker.py không lỗi
    echo - Thử build với: python -m PyInstaller run.py
)

echo.
pause
