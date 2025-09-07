@echo off
echo ========================================
echo Auto Clicker - Build GUI (Dễ sử dụng)
echo ========================================
echo.

echo 🎨 Cài đặt auto-py-to-exe (GUI cho PyInstaller)...
pip install auto-py-to-exe
echo.

echo 🚀 Mở giao diện build GUI...
echo.
echo 📋 Hướng dẫn sử dụng auto-py-to-exe:
echo    1. Script Location: Chọn file "run.py"
echo    2. Onefile: Chọn "One File" 
echo    3. Console Window: Chọn "Window Based"
echo    4. Additional Files: Add thư mục "image"
echo    5. Output Directory: Chọn "build/dist"
echo    6. Nhấn "Convert .py to .exe"
echo.

echo ⏳ Đang mở giao diện...
auto-py-to-exe

echo.
echo ✅ Nếu build thành công, file EXE sẽ ở trong build/dist/
echo.
pause
