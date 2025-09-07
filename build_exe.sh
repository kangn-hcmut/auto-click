#!/bin/bash

echo "========================================"
echo "Auto Clicker - Build EXE Script (Linux/Mac)"
echo "========================================"
echo

echo "Đang cài đặt PyInstaller..."
pip install pyinstaller

echo
echo "Đang build ứng dụng thành file executable..."
echo "Vui lòng đợi..."

pyinstaller \
    --onefile \
    --windowed \
    --name "AutoClicker-GameBot" \
    --add-data "image:image" \
    --distpath "build/dist" \
    --workpath "build/work" \
    --specpath "build" \
    run.py

echo
if [ -f "build/dist/AutoClicker-GameBot" ]; then
    echo "✅ Build thành công!"
    echo "📁 File executable: build/dist/AutoClicker-GameBot"
    echo "📋 Kích thước: $(ls -lh build/dist/AutoClicker-GameBot | awk '{print $5}')"
    echo
    echo "⚠️  Lưu ý: Khi chạy file executable, đảm bảo thư mục 'image' ở cùng vị trí!"
    echo
    echo "Mở thư mục build/dist? (y/n)"
    read choice
    if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
        if command -v xdg-open > /dev/null; then
            xdg-open "build/dist"
        elif command -v open > /dev/null; then
            open "build/dist"
        fi
    fi
else
    echo "❌ Build thất bại!"
    echo "Kiểm tra lỗi ở trên và thử lại."
fi

echo
read -p "Nhấn Enter để tiếp tục..."
