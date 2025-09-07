@echo off
echo ========================================
echo Fix PyInstaller Permission Error
echo ========================================
echo.

echo 🔧 Đang khắc phục lỗi quyền truy cập PyInstaller...
echo.

echo 📋 Bước 1: Dọn dẹp phiên bản cũ
pip uninstall pyinstaller pyinstaller-hooks-contrib altgraph pefile pywin32-ctypes -y
echo.

echo 📋 Bước 2: Dọn dẹp cache pip
pip cache purge
echo.

echo 📋 Bước 3: Tạo virtual environment (khuyến nghị)
if exist "venv" rmdir /s /q venv
python -m venv venv
call venv\Scripts\activate.bat
echo ✅ Virtual environment đã tạo
echo.

echo 📋 Bước 4: Cài đặt PyInstaller trong virtual environment
pip install --upgrade pip
pip install pyinstaller
echo.

echo 📋 Bước 5: Kiểm tra PyInstaller
venv\Scripts\pyinstaller.exe --version
if %ERRORLEVEL% EQU 0 (
    echo ✅ PyInstaller đã hoạt động trong virtual environment!
    echo.
    echo 🚀 Bắt đầu build...
    goto :build_in_venv
) else (
    echo ❌ Vẫn lỗi trong virtual environment
    goto :try_alternative
)

:build_in_venv
echo ========================================
echo Build trong Virtual Environment
echo ========================================

venv\Scripts\pyinstaller.exe ^
    --onefile ^
    --windowed ^
    --name "AutoClicker-GameBot" ^
    --add-data "image;image" ^
    --distpath "build/dist" ^
    --workpath "build/work" ^
    --specpath "build" ^
    --clean ^
    run.py

goto :check_result

:try_alternative
echo.
echo 📋 Phương pháp thay thế: Sử dụng cx_Freeze
pip install cx_freeze
echo.

echo 📋 Tạo setup.py cho cx_Freeze...
(
echo import sys
echo from cx_Freeze import setup, Executable
echo.
echo build_options = {
echo     'packages': ['tkinter', 'cv2', 'numpy', 'pyautogui', 'PIL'^],
echo     'include_files': [('image/', 'image/'^]
echo }
echo.
echo setup(
echo     name='AutoClicker-GameBot',
echo     version='0.2',
echo     description='Auto Clicker Game Bot',
echo     options={'build_exe': build_options},
echo     executables=[Executable('run.py', target_name='AutoClicker-GameBot.exe'^]
echo ^)
) > setup_cxfreeze.py

echo ✅ setup.py đã tạo
echo.

echo 🚀 Build với cx_Freeze...
python setup_cxfreeze.py build
echo.

echo 📁 Tìm file executable...
if exist "build\exe.*\AutoClicker-GameBot.exe" (
    echo ✅ Build thành công với cx_Freeze!
    for /d %%i in (build\exe.*) do (
        echo 📁 File EXE: %%i\AutoClicker-GameBot.exe
        if not exist "build\dist" mkdir "build\dist"
        copy "%%i\AutoClicker-GameBot.exe" "build\dist\"
    )
) else (
    echo ❌ cx_Freeze cũng thất bại
    goto :manual_instructions
)

:check_result
echo.
if exist "build\dist\AutoClicker-GameBot.exe" (
    echo ✅ BUILD THÀNH CÔNG!
    echo 📁 File EXE: build\dist\AutoClicker-GameBot.exe
    echo.
    echo 📦 Tạo package...
    if not exist "build\dist\package" mkdir "build\dist\package"
    copy "build\dist\AutoClicker-GameBot.exe" "build\dist\package\"
    xcopy "image" "build\dist\package\image" /E /I /Y
    copy "readme.md" "build\dist\package\"
    echo.
    echo ✅ Package hoàn thành: build\dist\package\
    echo.
    echo Mở thư mục? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" explorer "build\dist\package"
) else (
    goto :manual_instructions
)
goto :end

:manual_instructions
echo.
echo ========================================
echo ⚠️  TẤT CẢ PHƯƠNG PHÁP ĐỀU THẤT BẠI
echo ========================================
echo.
echo 💡 Hướng dẫn khắc phục thủ công:
echo.
echo 🔧 Phương pháp 1: Cài đặt Anaconda
echo    1. Download Anaconda từ: https://anaconda.com
echo    2. Cài đặt Anaconda
echo    3. Mở Anaconda Prompt
echo    4. Chạy: conda install pyinstaller
echo    5. Chạy: pyinstaller --onefile run.py
echo.
echo 🔧 Phương pháp 2: Chạy với quyền Administrator
echo    1. Nhấn Win + X
echo    2. Chọn "Windows PowerShell (Admin)"
echo    3. cd đến thư mục project
echo    4. Chạy lại script này
echo.
echo 🔧 Phương pháp 3: Cài đặt Python mới
echo    1. Gỡ Python hiện tại
echo    2. Download Python mới từ python.org
echo    3. Cài đặt với "Add to PATH"
echo    4. Chạy lại script
echo.
echo 🔧 Phương pháp 4: Sử dụng online converter
echo    1. Upload code lên replit.com hoặc colab.google.com
echo    2. Build trên cloud
echo    3. Download file EXE
echo.

:end
echo.
pause
