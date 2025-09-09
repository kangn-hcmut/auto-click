@echo off
echo ========================================
echo Auto Clicker v.0.3 - Schedule Automation
echo ========================================
echo.

echo 🕐 Lập lịch tự động cho Auto Clicker v.0.3
echo.
echo 💡 Chiến lược đề xuất:
echo    00:00-12:00: Starfall Mode (tích lũy ticket)
echo    12:00-24:00: Normal Mode (thu lượm tổng hợp)
echo.

echo 📋 Chọn phương pháp lập lịch:
echo 1. Task Scheduler (Windows) - Khuyến nghị
echo 2. Simple Time-based Script
echo 3. Manual Time Setting
echo.
set /p method="Chọn phương pháp (1/2/3): "

if "%method%"=="1" goto :task_scheduler
if "%method%"=="2" goto :simple_script
if "%method%"=="3" goto :manual_time
goto :invalid_choice

:task_scheduler
echo.
echo 🔧 Tạo Windows Task Scheduler...
echo.

REM Tạo script cho Starfall Mode
(
echo @echo off
echo cd /d "%~dp0.."
echo echo Starting Starfall Mode at %%time%%
echo scripts\switch_mode.bat starfall
echo python run.py --mode starfall --auto-stop 43200
) > "start_starfall.bat"

REM Tạo script cho Normal Mode  
(
echo @echo off
echo cd /d "%~dp0.."
echo echo Starting Normal Mode at %%time%%
echo scripts\switch_mode.bat normal
echo python run.py --mode normal --auto-stop 43200
) > "start_normal.bat"

echo ✅ Scripts đã tạo: start_starfall.bat, start_normal.bat
echo.

echo 📝 Tạo Task Scheduler commands...
echo.
echo Chạy các lệnh sau trong Command Prompt (Administrator):
echo.
echo REM Tạo task cho Starfall Mode (0:00 AM)
echo schtasks /create /tn "AutoClicker_Starfall" /tr "%cd%\start_starfall.bat" /sc daily /st 00:00
echo.
echo REM Tạo task cho Normal Mode (12:00 PM) 
echo schtasks /create /tn "AutoClicker_Normal" /tr "%cd%\start_normal.bat" /sc daily /st 12:00
echo.
echo 💡 Để xóa tasks:
echo schtasks /delete /tn "AutoClicker_Starfall" /f
echo schtasks /delete /tn "AutoClicker_Normal" /f
echo.

echo Tự động tạo tasks? (cần quyền Administrator) (Y/N)
set /p auto_create=
if /i "%auto_create%"=="Y" (
    echo 🔧 Tạo tasks...
    schtasks /create /tn "AutoClicker_Starfall" /tr "%cd%\start_starfall.bat" /sc daily /st 00:00 /f
    schtasks /create /tn "AutoClicker_Normal" /tr "%cd%\start_normal.bat" /sc daily /st 12:00 /f
    
    if errorlevel 1 (
        echo ❌ Lỗi tạo tasks! Cần chạy với quyền Administrator
    ) else (
        echo ✅ Tasks đã được tạo thành công!
        echo 📋 Kiểm tra: Task Scheduler → Task Scheduler Library
    )
)
goto :end

:simple_script
echo.
echo 🔄 Tạo Simple Time-based Script...
echo.

(
echo @echo off
echo :loop
echo echo ========================================
echo echo Auto Clicker v.0.3 - Time-based Automation
echo echo Current time: %%time%%
echo echo ========================================
echo.
echo REM Lấy giờ hiện tại
echo for /f "tokens=1 delims=:" %%%%i in ^("%%time%%"^) do set hour=%%%%i
echo set /a hour=%%hour%%
echo.
echo REM Kiểm tra thời gian và chạy chế độ tương ứng
echo if %%hour%% geq 0 if %%hour%% lss 12 ^(
echo     echo 🌟 Starfall Time ^(00:00-12:00^) - Starting Starfall Mode...
echo     call scripts\switch_mode.bat starfall
echo     python run.py --mode starfall --duration 12h
echo ^) else ^(
echo     echo 🏆 Normal Time ^(12:00-24:00^) - Starting Normal Mode...
echo     call scripts\switch_mode.bat normal  
echo     python run.py --mode normal --duration 12h
echo ^)
echo.
echo echo Sleeping for 1 hour before next check...
echo timeout /t 3600 /nobreak ^> nul
echo goto :loop
) > "auto_scheduler.bat"

echo ✅ Script tự động đã tạo: auto_scheduler.bat
echo.
echo 🚀 Để chạy:
echo    auto_scheduler.bat
echo.
echo 💡 Script sẽ:
echo    - Kiểm tra giờ hiện tại mỗi giờ
echo    - 00:00-12:00: Chạy Starfall Mode  
echo    - 12:00-24:00: Chạy Normal Mode
echo.
goto :end

:manual_time
echo.
echo ⏰ Manual Time Setting
echo.
echo Đặt thời gian bắt đầu cho từng chế độ:
echo.
set /p starfall_start="Starfall Mode bắt đầu lúc (HH:MM, VD: 00:00): "
set /p starfall_duration="Starfall Mode chạy trong (giờ, VD: 12): "
set /p normal_start="Normal Mode bắt đầu lúc (HH:MM, VD: 12:00): "
set /p normal_duration="Normal Mode chạy trong (giờ, VD: 12): "

echo.
echo 📝 Cấu hình của bạn:
echo    Starfall Mode: %starfall_start% (chạy %starfall_duration% giờ)
echo    Normal Mode: %normal_start% (chạy %normal_duration% giờ)
echo.

(
echo @echo off
echo echo Custom Schedule - Auto Clicker v.0.3
echo echo Starfall: %starfall_start% ^(%starfall_duration%h^)
echo echo Normal: %normal_start% ^(%normal_duration%h^) 
echo echo.
echo echo 💡 Cài đặt Task Scheduler theo lịch trình tùy chỉnh:
echo echo.
echo echo schtasks /create /tn "AutoClicker_Custom_Starfall" /tr "%%cd%%\start_starfall.bat" /sc daily /st %starfall_start%
echo echo schtasks /create /tn "AutoClicker_Custom_Normal" /tr "%%cd%%\start_normal.bat" /sc daily /st %normal_start%
echo echo.
echo pause
) > "custom_schedule.bat"

echo ✅ Custom schedule script đã tạo: custom_schedule.bat
goto :end

:invalid_choice
echo ❌ Lựa chọn không hợp lệ!
goto :end

:end
echo.
echo ========================================
echo 📋 Tổng kết Schedule Automation
echo ========================================
echo.
echo 📁 Files đã tạo:
if exist "start_starfall.bat" echo    ✅ start_starfall.bat
if exist "start_normal.bat" echo    ✅ start_normal.bat  
if exist "auto_scheduler.bat" echo    ✅ auto_scheduler.bat
if exist "custom_schedule.bat" echo    ✅ custom_schedule.bat
echo.
echo 💡 Lưu ý quan trọng:
echo    - Đảm bảo máy tính không sleep/hibernate
echo    - Game phải mở và sẵn sàng
echo    - Kiểm tra scripts hoạt động thủ công trước
echo    - Có thể điều chỉnh thời gian trong các file .bat
echo.
echo 🔧 Quản lý Tasks:
echo    - Xem: Task Scheduler → Task Scheduler Library
echo    - Xóa: schtasks /delete /tn "task_name" /f
echo    - Test: schtasks /run /tn "task_name"
echo.
echo 📊 Monitor:
echo    - Sử dụng scripts\monitor_performance.py để theo dõi
echo    - Check log files trong thư mục gốc
echo.
pause
