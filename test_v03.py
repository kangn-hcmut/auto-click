#!/usr/bin/env python3
"""
Script test cho Feature v.0.3
"""

import os
import json
import sys

def test_config_files():
    """Test xem các file cấu hình có tồn tại không"""
    print("🧪 Testing configuration files...")
    
    config_dir = "config"
    if not os.path.exists(config_dir):
        print("❌ Thư mục config không tồn tại")
        return False
    
    # Test starfall config
    starfall_config = os.path.join(config_dir, "starfall_config.json")
    if os.path.exists(starfall_config):
        try:
            with open(starfall_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ starfall_config.json: {config['mode']} mode, confidence={config['confidence']}")
        except Exception as e:
            print(f"❌ Lỗi đọc starfall_config.json: {e}")
            return False
    else:
        print("❌ starfall_config.json không tồn tại")
        return False
    
    # Test normal config
    normal_config = os.path.join(config_dir, "normal_config.json")
    if os.path.exists(normal_config):
        try:
            with open(normal_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ normal_config.json: {config['mode']} mode, confidence={config['confidence']}")
        except Exception as e:
            print(f"❌ Lỗi đọc normal_config.json: {e}")
            return False
    else:
        print("❌ normal_config.json không tồn tại")
        return False
    
    return True

def test_image_files():
    """Test xem các file hình ảnh có tồn tại không"""
    print("\n🧪 Testing image files...")
    
    image_dir = "image"
    if not os.path.exists(image_dir):
        print("❌ Thư mục image không tồn tại")
        return False
    
    # Images cho Normal mode
    normal_images = ["gold2.png", "gold.png", "coin.png", "Gems.png", "OK.png", "Claim.png"]
    # Images cho Starfall mode
    starfall_images = ["ads.png", "star_claim.png"]
    
    all_images = set(normal_images + starfall_images)
    
    missing_images = []
    for img in all_images:
        img_path = os.path.join(image_dir, img)
        if os.path.exists(img_path):
            print(f"✅ {img}")
        else:
            print(f"❌ {img} - THIẾU")
            missing_images.append(img)
    
    if missing_images:
        print(f"\n⚠️  Thiếu {len(missing_images)} hình ảnh: {', '.join(missing_images)}")
        return False
    
    return True

def test_scripts():
    """Test xem các script có tồn tại không"""
    print("\n🧪 Testing script files...")
    
    scripts_dir = "scripts"
    if not os.path.exists(scripts_dir):
        print("❌ Thư mục scripts không tồn tại")
        return False
    
    required_scripts = [
        "test_starfall.bat",
        "switch_mode.bat", 
        "auto_setup.bat",
        "build_v3.bat",
        "test_recognition.py",
        "monitor_performance.py",
        "schedule_auto.bat"
    ]
    
    missing_scripts = []
    for script in required_scripts:
        script_path = os.path.join(scripts_dir, script)
        if os.path.exists(script_path):
            print(f"✅ {script}")
        else:
            print(f"❌ {script} - THIẾU")
            missing_scripts.append(script)
    
    if missing_scripts:
        print(f"\n⚠️  Thiếu {len(missing_scripts)} script: {', '.join(missing_scripts)}")
        return False
    
    return True

def test_import():
    """Test xem có thể import được không"""
    print("\n🧪 Testing imports...")
    
    try:
        # Test import run.py functionality
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Test import auto_clicker
        from auto_clicker import AutoClickerApp
        print("✅ AutoClickerApp import thành công")
        
        # Test import tkinter
        import tkinter as tk
        print("✅ tkinter import thành công")
        
        # Test import các thư viện khác
        import cv2
        print("✅ cv2 import thành công")
        
        import pyautogui
        print("✅ pyautogui import thành công")
        
        import numpy as np
        print("✅ numpy import thành công")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 50)
    print("Auto Clicker v.0.3 - Test Suite")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run tests
    if not test_config_files():
        all_tests_passed = False
    
    if not test_image_files():
        all_tests_passed = False
    
    if not test_scripts():
        all_tests_passed = False
    
    if not test_import():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 TẤT CẢ TEST PASSED! Feature v.0.3 sẵn sàng sử dụng!")
        print("\n🚀 Các cách chạy:")
        print("   python run.py                    # GUI mặc định")
        print("   python run.py --mode normal      # Normal Mode")
        print("   python run.py --mode starfall    # Starfall Mode") 
        print("   python run.py --debug            # Debug Mode")
        print("   scripts\\switch_mode.bat normal   # Chuyển chế độ")
    else:
        print("❌ MỘT SỐ TEST FAILED! Cần khắc phục trước khi sử dụng.")
    print("=" * 50)

if __name__ == "__main__":
    main()
