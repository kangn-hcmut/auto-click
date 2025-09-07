@echo off
echo ========================================
echo Auto Clicker - Build EXE Script
echo ========================================
echo.

echo Đang cài đặt PyInstaller...
pip install pyinstaller

echo.
echo Đang build ứng dụng thành file EXE...
echo Vui lòng đợi...

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "AutoClicker-GameBot" ^
    --icon=image/coin.png ^
    --add-data "image;image" ^
    --distpath "build/dist" ^
    --workpath "build/work" ^
    --specpath "build" ^
    run.py

echo.
if exist "build\dist\AutoClicker-GameBot.exe" (
    echo ✅ Build thành công!
    echo 📁 File EXE: build\dist\AutoClicker-GameBot.exe
    echo 📋 Kích thước: 
    dir "build\dist\AutoClicker-GameBot.exe" | find "AutoClicker-GameBot.exe"
    echo.
    echo ⚠️  Lưu ý: Khi chạy file EXE, đảm bảo thư mục 'image' ở cùng vị trí!
    echo.
    echo Mở thư mục build\dist? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" explorer "build\dist"
) else (
    echo ❌ Build thất bại!
    echo Kiểm tra lỗi ở trên và thử lại.
)

echo.
pause
