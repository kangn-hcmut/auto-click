#!/usr/bin/env python3
"""
Test nhận diện hình ảnh cho v.0.3
"""

import cv2
import numpy as np
import pyautogui
import os
import sys
import json
import argparse
from PIL import Image

def test_single_image(image_name, confidence=0.8):
    """Test nhận diện một hình ảnh cụ thể"""
    print(f"🔍 Test nhận diện: {image_name}")
    
    image_dir = "../image"
    image_path = os.path.join(image_dir, image_name)
    
    if not os.path.exists(image_path):
        print(f"❌ Không tìm thấy file: {image_name}")
        return False
        
    try:
        # Đọc hình ảnh mẫu
        template = cv2.imread(image_path)
        if template is None:
            print(f"❌ Không thể đọc file: {image_name}")
            return False
        
        h, w = template.shape[:2]
        print(f"✅ Đọc file thành công: {w}x{h} pixels")
        
        # Chụp màn hình
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        print(f"✅ Chụp màn hình: {screenshot.size}")
        
        # Test nhận diện
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= confidence)
        
        if len(locations[0]) > 0:
            count = len(locations[0])
            max_val = np.max(result)
            y, x = locations[0][0], locations[1][0]
            print(f"✅ Tìm thấy {count} vị trí khớp")
            print(f"   Độ chính xác tối đa: {max_val:.3f}")
            print(f"   Vị trí tốt nhất: ({x}, {y})")
            return True
        else:
            max_val = np.max(result)
            print(f"❌ Không tìm thấy (độ chính xác tối đa: {max_val:.3f})")
            print(f"   Thử giảm confidence xuống {max_val:.3f} hoặc thấp hơn")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi test {image_name}: {e}")
        return False

def test_starfall_images():
    """Test tất cả hình ảnh cho starfall mode"""
    print("=== Test Starfall Mode Images ===")
    
    required_images = ["ads.png", "Claim.png"]
    optional_images = ["starfall.png"]
    
    print(f"\n🔍 Test hình ảnh bắt buộc:")
    all_required_ok = True
    for img in required_images:
        success = test_single_image(img, confidence=0.7)
        if not success:
            all_required_ok = False
        print()
    
    print(f"🔍 Test hình ảnh tùy chọn:")
    for img in optional_images:
        if os.path.exists(f"../image/{img}"):
            test_single_image(img, confidence=0.7)
        else:
            print(f"⚠️  {img}: Không có (có thể thêm sau)")
        print()
    
    return all_required_ok

def test_normal_images():
    """Test tất cả hình ảnh cho normal mode"""
    print("=== Test Normal Mode Images ===")
    
    normal_images = ["gold2.png", "gold.png", "coin.png", "Gems.png", "OK.png", "Claim.png"]
    
    all_ok = True
    for img in normal_images:
        success = test_single_image(img, confidence=0.8)
        if not success:
            all_ok = False
        print()
    
    return all_ok

def test_config_files():
    """Test các file cấu hình"""
    print("=== Test Config Files ===")
    
    config_dir = "../config"
    configs = ["normal_config.json", "starfall_config.json"]
    
    for config in configs:
        path = os.path.join(config_dir, config)
        print(f"\n🔍 Test {config}:")
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                print(f"✅ File hợp lệ")
                print(f"   Mode: {data.get('mode', 'N/A')}")
                print(f"   Confidence: {data.get('confidence', 'N/A')}")
                print(f"   Ads wait: {data.get('ads_wait_time', 'N/A')} seconds")
                print(f"   Images: {len(data.get('images', []))} files")
            except Exception as e:
                print(f"❌ Lỗi đọc file: {e}")
        else:
            print(f"❌ Không tìm thấy file")

def main():
    parser = argparse.ArgumentParser(description='Test nhận diện hình ảnh cho Auto Clicker v.0.3')
    parser.add_argument('--image', help='Test một hình ảnh cụ thể')
    parser.add_argument('--confidence', type=float, default=0.8, help='Độ chính xác (0.0-1.0)')
    parser.add_argument('--mode', choices=['normal', 'starfall', 'all'], default='all', 
                       help='Test chế độ cụ thể')
    
    args = parser.parse_args()
    
    print("🔍 Auto Clicker v.0.3 - Image Recognition Test")
    print("=" * 50)
    
    if args.image:
        # Test một hình ảnh cụ thể
        test_single_image(args.image, args.confidence)
    else:
        # Test theo chế độ
        if args.mode in ['all', 'normal']:
            normal_ok = test_normal_images()
            
        if args.mode in ['all', 'starfall']:
            starfall_ok = test_starfall_images()
        
        # Test config files
        test_config_files()
        
        print("\n" + "=" * 50)
        print("📋 Tổng kết:")
        if args.mode in ['all', 'normal']:
            print(f"Normal Mode: {'✅ OK' if normal_ok else '❌ Có lỗi'}")
        if args.mode in ['all', 'starfall']:
            print(f"Starfall Mode: {'✅ OK' if starfall_ok else '❌ Có lỗi'}")
        
        print("\n💡 Gợi ý:")
        print("- Nếu không tìm thấy hình ảnh, kiểm tra thư mục image/")
        print("- Nếu độ chính xác thấp, thử giảm confidence trong config")
        print("- Đảm bảo game hiển thị đầy đủ trên màn hình")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Test bị dừng bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        print("\n💡 Đảm bảo đã cài đặt: pip install opencv-python pyautogui pillow numpy")
