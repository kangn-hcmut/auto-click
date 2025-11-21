@echo off
echo ========================================
echo Auto Clicker v.0.3 - Build EXE with Starfall Mode
echo ========================================
echo.

echo 🚀 Build Auto Clicker v.0.3 với tính năng Starfall Mode...
echo.

echo 📋 Bước 1: Kiểm tra cài đặt...
cd ..

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    pause
    exit /b 1
)

REM Check dependencies
echo ✅ Python OK - Kiểm tra dependencies...
python -c "import cv2, pyautogui, numpy, PIL" >nul 2>&1
if errorlevel 1 (
    echo ❌ Thiếu dependencies! Chạy install_fix.bat trước
    pause
    exit /b 1
)

echo ✅ Dependencies OK

echo.
echo 📋 Bước 2: Cài đặt/Cập nhật PyInstaller...
pip install --upgrade pyinstaller

echo.
echo 📋 Bước 3: Tạo cấu hình v.0.3...
if not exist "config" (
    echo 🔧 Tạo cấu hình v.0.3...
    scripts\auto_setup.bat
)

echo.
echo 📋 Bước 4: Build EXE cho v.0.3...
echo 🔨 Đang build với tính năng Starfall Mode...

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "AutoClicker-GameBot-v0.3" ^
    --icon=image/coin.png ^
    --add-data "image;image" ^
    --add-data "config;config" ^
    --add-data "scripts;scripts" ^
    --distpath "build/dist" ^
    --workpath "build/work" ^
    --specpath "build" ^
    --clean ^
    run.py

echo.
if exist "build\dist\AutoClicker-GameBot-v0.3.exe" (
    echo ✅ Build v.0.3 thành công!
    echo 📁 File EXE: build\dist\AutoClicker-GameBot-v0.3.exe
    echo.
    
    echo 📦 Tạo package v.0.3 hoàn chỉnh...
    if not exist "build\dist\package-v0.3" mkdir "build\dist\package-v0.3"
    
    REM Copy EXE
    copy "build\dist\AutoClicker-GameBot-v0.3.exe" "build\dist\package-v0.3\"
    
    REM Copy images
    xcopy "image" "build\dist\package-v0.3\image" /E /I /Y
    
    REM Copy configs
    xcopy "config" "build\dist\package-v0.3\config" /E /I /Y
    
    REM Copy scripts
    xcopy "scripts" "build\dist\package-v0.3\scripts" /E /I /Y
    
    REM Copy docs
    copy "readme.md" "build\dist\package-v0.3\"
    copy "khac_phuc_loi.md" "build\dist\package-v0.3\" 2>nul
    
    REM Tạo hướng dẫn sử dụng v.0.3
    (
    echo # Auto Clicker v.0.3 - Hướng dẫn sử dụng
    echo.
    echo ## 🎯 Tính năng mới v.0.3:
    echo - Normal Mode: Thu lượm gold/coin + gems + ads
    echo - Starfall Mode: Chỉ tập trung xem ads để nhận starfall ticket
    echo.
    echo ## 🚀 Cách sử dụng:
    echo.
    echo ### Phương pháp 1: Chạy trực tiếp
    echo 1. Chạy: AutoClicker-GameBot-v0.3.exe
    echo 2. Chọn chế độ trong GUI:
    echo    - "Normal Mode" hoặc "Starfall Mode"
    echo 3. Click "Bắt đầu"
    echo.
    echo ### Phương pháp 2: Sử dụng scripts
    echo 1. Test starfall: scripts\test_starfall.bat
    echo 2. Chuyển chế độ: scripts\switch_mode.bat starfall
    echo 3. Chạy EXE
    echo.
    echo ## 📁 Cấu trúc package:
    echo - AutoClicker-GameBot-v0.3.exe  # File chính
    echo - image/                        # Hình ảnh nhận diện
    echo - config/                       # File cấu hình 2 chế độ
    echo - scripts/                      # Scripts hỗ trợ
    echo - readme.md                     # Hướng dẫn đầy đủ
    echo.
    echo ## ⚠️  Lưu ý:
    echo - Đảm bảo tất cả thư mục con ở cùng vị trí với EXE
    echo - Cần có hình ảnh ads.png để chạy Starfall Mode
    echo - Di chuyển chuột tới góc trái trên để dừng khẩn cấp
    echo.
    echo ## 🔧 Cấu hình:
    echo - Normal Mode: config\normal_config.json
    echo - Starfall Mode: config\starfall_config.json
    echo.
    echo ## 📊 So sánh chế độ:
    echo Normal Mode: Thu lượm toàn diện ^(chậm hơn^)
    echo Starfall Mode: Tập trung starfall ticket ^(nhanh hơn^)
    ) > "build\dist\package-v0.3\USAGE_v0.3.md"
    
    echo ✅ Package v.0.3 hoàn thành!
    echo.
    echo 📋 Kích thước và thông tin:
    dir "build\dist\AutoClicker-GameBot-v0.3.exe" | find ".exe"
    echo.
    echo 📁 Package location: build\dist\package-v0.3\
    echo 📄 Files in package:
    dir "build\dist\package-v0.3" /b
    echo.
    echo 🎯 Tính năng v.0.3:
    echo    ✅ Normal Mode ^(như v.0.2^)
    echo    ✅ Starfall Mode ^(mới^)
    echo    ✅ Mode switching scripts
    echo    ✅ Config files cho 2 chế độ
    echo    ✅ Test và debug tools
    echo    ✅ Performance monitoring
    echo.
    echo Mở thư mục package? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" explorer "build\dist\package-v0.3"
) else (
    echo ❌ Build v.0.3 thất bại!
    echo 💡 Thử:
    echo    1. build_exe_fix.bat
    echo    2. Hoặc build_nuitka.bat
    echo    3. Hoặc fix_pyinstaller_permission.bat
)

echo.
pause
