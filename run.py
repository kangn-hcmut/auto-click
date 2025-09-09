#!/usr/bin/env python3
"""
Script khởi chạy ứng dụng Auto Clicker v.0.3
Hỗ trợ Starfall Mode và Normal Mode
"""

import sys
import os
import argparse
import json

# Thêm thư mục hiện tại vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_config(config_path):
    """Tải cấu hình từ file JSON"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Không tìm thấy file cấu hình: {config_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Lỗi đọc file cấu hình: {e}")
        return None

def main():
    """Hàm main với hỗ trợ argument parsing"""
    parser = argparse.ArgumentParser(description='Auto Clicker v.0.3 - Game Bot')
    parser.add_argument('--mode', choices=['normal', 'starfall'], 
                       help='Chế độ hoạt động (normal hoặc starfall)')
    parser.add_argument('--config', type=str,
                       help='Đường dẫn file cấu hình JSON')
    parser.add_argument('--debug', action='store_true',
                       help='Bật chế độ debug')
    
    args = parser.parse_args()
    
    # Xác định cấu hình
    config = None
    if args.config:
        config = load_config(args.config)
    elif args.mode:
        config_file = f"config/{args.mode}_config.json"
        config = load_config(config_file)
    
    # Hiển thị thông tin khởi chạy
    print("=" * 50)
    print("Auto Clicker v.0.3 - Game Bot")
    print("=" * 50)
    
    if args.mode:
        mode_name = "Starfall Mode" if args.mode == "starfall" else "Normal Mode"
        print(f"Chế độ: {mode_name}")
    
    if config:
        print(f"Cấu hình: {config.get('mode', 'unknown').title()} Mode")
        print(f"Độ chính xác: {config.get('confidence', 0.8)}")
        print(f"Chu kì delay: {config.get('cycle_delay', 5)} giây")
        print("Logic: Quét liên tục cho Claim.png (không cố định thời gian ads)")
    
    if args.debug:
        print("Chế độ debug: BẬT")
    
    print("Đảm bảo rằng các hình ảnh đã có trong thư mục 'image'")
    print("Nhấn Ctrl+C để thoát ứng dụng")
    print("=" * 50)

try:
    from auto_clicker import AutoClickerApp
    import tkinter as tk
    
    if __name__ == "__main__":
        # Parse arguments
        parser = argparse.ArgumentParser(description='Auto Clicker v.0.3 - Game Bot')
        parser.add_argument('--mode', choices=['normal', 'starfall'], 
                           help='Chế độ hoạt động (normal hoặc starfall)')
        parser.add_argument('--config', type=str,
                           help='Đường dẫn file cấu hình JSON')
        parser.add_argument('--debug', action='store_true',
                           help='Bật chế độ debug')
        
        args = parser.parse_args()
        
        # Tải cấu hình
        config = None
        if args.config:
            config = load_config(args.config)
        elif args.mode:
            config_file = f"config/{args.mode}_config.json"
            config = load_config(config_file)
        
        # Hiển thị thông tin
        main()
        
        # Khởi chạy GUI
        root = tk.Tk()
        app = AutoClickerApp(root, mode=args.mode, config=config, debug=args.debug)
        root.mainloop()
        
except ImportError as e:
    print(f"Lỗi import: {e}")
    print("Vui lòng cài đặt các thư viện cần thiết:")
    print("pip install -r requirements.txt")
except Exception as e:
    print(f"Lỗi khi chạy ứng dụng: {e}")
