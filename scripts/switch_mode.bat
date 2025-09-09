@echo off
echo ========================================
echo Auto Clicker v.0.3 - Switch Mode
echo ========================================
echo.

set "mode=%1"

if "%mode%"=="" (
    echo 💡 Cách sử dụng: scripts\switch_mode.bat [normal/starfall]
    echo.
    echo 🎯 Chế độ hiện có:
    echo    normal   - Thu lượm gold/coin + gems + ads
    echo    starfall - Chỉ xem ads để nhận starfall ticket
    echo.
    set /p mode="Chọn chế độ (normal/starfall): "
)

if /i "%mode%"=="normal" goto :normal_mode
if /i "%mode%"=="starfall" goto :starfall_mode

echo ❌ Chế độ không hợp lệ: %mode%
echo 💡 Chỉ hỗ trợ: normal hoặc starfall
pause
exit /b 1

:normal_mode
echo 🔄 Chuyển sang Normal Mode...
echo.
echo ✅ Cấu hình Normal Mode:
echo    - Thu lượm gold2.png, gold.png, coin.png
echo    - Thu lượm Gems.png
echo    - Xem ads và claim phần thưởng
echo    - Thời gian chờ ads: 30 giây
echo    - Độ chính xác: 0.8
echo.
if exist "..\config\normal_config.json" (
    echo 📋 Sử dụng cấu hình: config\normal_config.json
    type "..\config\normal_config.json"
) else (
    echo ⚠️  File cấu hình Normal chưa có, tạo mặc định...
    call auto_setup.bat
)
echo.
echo ✅ Đã chuyển sang Normal Mode!
echo 🚀 Chạy ứng dụng: python run.py
goto :end

:starfall_mode
echo 🌟 Chuyển sang Starfall Mode...
echo.
echo ✅ Cấu hình Starfall Mode:
echo    - Chỉ tìm ads.png để xem ads
echo    - Claim starfall ticket
echo    - Bỏ qua thu lượm gold/coin/gems
echo    - Thời gian chờ ads: 45 giây
echo    - Độ chính xác: 0.7 (thấp hơn để dễ tìm)
echo.
if exist "..\config\starfall_config.json" (
    echo 📋 Sử dụng cấu hình: config\starfall_config.json
    type "..\config\starfall_config.json"
) else (
    echo ⚠️  File cấu hình Starfall chưa có, tạo mặc định...
    call auto_setup.bat
)
echo.
echo ✅ Đã chuyển sang Starfall Mode!
echo 🚀 Chạy ứng dụng: python run.py

:end
echo.
echo 📝 Ghi chú:
echo    - Chế độ hiện tại sẽ được ghi nhớ trong ứng dụng
echo    - Có thể chuyển đổi chế độ trong GUI
echo    - Xem log để theo dõi hoạt động
echo.
pause
