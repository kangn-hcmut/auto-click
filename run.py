#!/usr/bin/env python3
"""
Script khởi chạy ứng dụng Auto Clicker
"""

import sys
import os

# Thêm thư mục hiện tại vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from auto_clicker import main
    
    if __name__ == "__main__":
        print("Đang khởi chạy Auto Clicker...")
        print("Đảm bảo rằng các hình ảnh đã có trong thư mục 'image'")
        print("Nhấn Ctrl+C để thoát ứng dụng")
        main()
        
except ImportError as e:
    print(f"Lỗi import: {e}")
    print("Vui lòng cài đặt các thư viện cần thiết:")
    print("pip install -r requirements.txt")
except Exception as e:
    print(f"Lỗi khi chạy ứng dụng: {e}")
