@echo off
echo ========================================
echo Auto Clicker - Build với Nuitka (Thay thế PyInstaller)
echo ========================================
echo.

echo 🔧 Cài đặt Nuitka...
pip install nuitka
echo.

echo 🚀 Build với Nuitka (tạo file EXE nhanh hơn, nhỏ hơn)...
python -m nuitka ^
    --onefile ^
    --windows-disable-console ^
    --enable-plugin=tk-inter ^
    --include-data-dir=image=image ^
    --output-dir=build/nuitka ^
    --output-filename=AutoClicker-GameBot.exe ^
    run.py

echo.
if exist "build\nuitka\AutoClicker-GameBot.exe" (
    echo ✅ Build thành công với Nuitka!
    echo 📁 File EXE: build\nuitka\AutoClicker-GameBot.exe
    echo.
    echo 📦 Tạo package...
    if not exist "build\nuitka\package" mkdir "build\nuitka\package"
    copy "build\nuitka\AutoClicker-GameBot.exe" "build\nuitka\package\"
    xcopy "image" "build\nuitka\package\image" /E /I /Y
    copy "readme.md" "build\nuitka\package\"
    echo.
    echo ✅ Package hoàn thành: build\nuitka\package\
    echo 📋 So sánh kích thước:
    if exist "build\dist\AutoClicker-GameBot.exe" (
        echo    PyInstaller: 
        dir "build\dist\AutoClicker-GameBot.exe" | find ".exe"
    )
    echo    Nuitka: 
    dir "build\nuitka\AutoClicker-GameBot.exe" | find ".exe"
    echo.
    echo Mở thư mục? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" explorer "build\nuitka\package"
) else (
    echo ❌ Nuitka build thất bại!
    echo 💡 Thử cài đặt Microsoft Visual C++ Redistributable
    echo    Download từ: https://aka.ms/vs/17/release/vc_redist.x64.exe
)

echo.
pause
