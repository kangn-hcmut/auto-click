@echo off
echo ========================================
echo Auto Clicker v.0.3 - Test Starfall Mode
echo ========================================
echo.

echo 🔍 Test nhận diện hình ảnh Starfall Mode...
echo.

echo 📋 Bước 1: Kiểm tra các file hình ảnh cần thiết...
set "image_dir=..\image"

echo ✅ Kiểm tra ads.png...
if exist "%image_dir%\ads.png" (
    echo    ✅ ads.png - OK
) else (
    echo    ❌ ads.png - KHÔNG TÌM THẤY
    echo    💡 Cần thêm hình ảnh nút ads
)

echo ✅ Kiểm tra Claim.png...
if exist "%image_dir%\Claim.png" (
    echo    ✅ Claim.png - OK
) else (
    echo    ❌ Claim.png - KHÔNG TÌM THẤY
    echo    💡 Cần thêm hình ảnh nút claim
)

echo ✅ Kiểm tra starfall.png (tùy chọn)...
if exist "%image_dir%\starfall.png" (
    echo    ✅ starfall.png - OK
) else (
    echo    ⚠️  starfall.png - Không có (tùy chọn)
    echo    💡 Có thể thêm để nhận diện starfall ticket
)

echo.
echo 📋 Bước 2: Test nhận diện hình ảnh...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    echo 💡 Vui lòng cài đặt Python từ python.org
    pause
    exit /b 1
)

echo 🐍 Python OK - Chạy test nhận diện...
cd ..
python demo_test.py

echo.
echo 📋 Bước 3: Test cấu hình Starfall Mode...
if exist "config\starfall_config.json" (
    echo ✅ File cấu hình starfall_config.json đã có
    type "config\starfall_config.json"
) else (
    echo ⚠️  File cấu hình chưa có - sẽ tạo mặc định
    scripts\auto_setup.bat
)

echo.
echo ========================================
echo 🎯 Kết quả test:
echo ========================================
echo.
echo ✅ Nếu tất cả hình ảnh được nhận diện thành công,
echo    Starfall Mode sẽ hoạt động bình thường
echo.
echo 💡 Để chạy Starfall Mode:
echo    1. scripts\switch_mode.bat starfall
echo    2. python run.py
echo.
echo 💡 Để chuyển về Normal Mode:
echo    1. scripts\switch_mode.bat normal
echo    2. python run.py
echo.
pause
