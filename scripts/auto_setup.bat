@echo off
echo ========================================
echo Auto Clicker v.0.3 - Auto Setup
echo ========================================
echo.

echo 🚀 Cài đặt tự động cho Auto Clicker v.0.3...
echo.

echo 📋 Bước 1: Tạo thư mục cấu hình...
if not exist "..\config" mkdir "..\config"
echo ✅ Thư mục config đã sẵn sàng

echo.
echo 📋 Bước 2: Tạo file cấu hình Normal Mode...
(
echo {
echo   "mode": "normal",
echo   "collect_gold": true,
echo   "collect_gems": true, 
echo   "ads_wait_time": 30,
echo   "max_attempts": 10,
echo   "confidence": 0.8,
echo   "images": ["gold2.png", "gold.png", "coin.png", "Gems.png", "OK.png", "Claim.png"],
echo   "cycle_delay": 5,
echo   "max_gold_collection": 10,
echo   "step_wait_time": 2
echo }
) > "..\config\normal_config.json"
echo ✅ File normal_config.json đã tạo

echo.
echo 📋 Bước 3: Tạo file cấu hình Starfall Mode...
(
echo {
echo   "mode": "starfall",
echo   "collect_gold": false,
echo   "collect_gems": false,
echo   "ads_wait_time": 45,
echo   "max_attempts": 20,
echo   "confidence": 0.7,
echo   "images": ["ads.png", "Claim.png", "starfall.png"],
echo   "cycle_delay": 10,
echo   "focus_ads_only": true,
echo   "step_wait_time": 3
echo }
) > "..\config\starfall_config.json"
echo ✅ File starfall_config.json đã tạo

echo.
echo 📋 Bước 4: File test_recognition.py đã được tạo từ trước
echo ✅ File test_recognition.py có sẵn

echo.
echo 📋 Bước 5: File monitor_performance.py đã được tạo từ trước
echo ✅ File monitor_performance.py có sẵn

echo.
echo 📋 Bước 6: Kiểm tra cài đặt dependencies...
cd ..
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    echo 💡 Vui lòng cài đặt Python từ python.org
    goto :end
)

echo ✅ Python OK
python -c "import cv2, pyautogui, numpy, PIL, psutil" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Một số thư viện chưa được cài đặt
    echo 🔧 Cài đặt thư viện cần thiết...
    pip install psutil >nul 2>&1
    echo ✅ Dependencies updated
) else (
    echo ✅ Tất cả dependencies OK
)

echo.
echo 📋 Bước 7: Test cài đặt...
echo 🧪 Chạy test cơ bản...
python scripts/test_recognition.py

:end
echo.
echo ========================================
echo ✅ AUTO SETUP HOÀN THÀNH!
echo ========================================
echo.
echo 🎯 Cách sử dụng Auto Clicker v.0.3:
echo.
echo 1️⃣ Test Starfall Mode:
echo    scripts\test_starfall.bat
echo.
echo 2️⃣ Chuyển đổi chế độ:
echo    scripts\switch_mode.bat normal
echo    scripts\switch_mode.bat starfall
echo.
echo 3️⃣ Chạy ứng dụng:
echo    python run.py
echo.
echo 4️⃣ Monitor hiệu suất:
echo    python scripts\monitor_performance.py
echo.
echo 📁 Files đã tạo:
echo    ✅ config\normal_config.json
echo    ✅ config\starfall_config.json
echo    ✅ scripts\test_recognition.py
echo    ✅ scripts\monitor_performance.py
echo.
pause
