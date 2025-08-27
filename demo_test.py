#!/usr/bin/env python3
"""
Script demo để test chức năng nhận diện hình ảnh
"""

import cv2
import numpy as np
import pyautogui
import os
from PIL import Image

def test_image_recognition():
    """Test chức năng nhận diện hình ảnh"""
    print("Demo Test - Nhận diện hình ảnh")
    print("=" * 40)
    
    image_dir = "image"
    confidence = 0.8
    
    # Danh sách hình ảnh cần test
    test_images = ["Gems.png", "OK.png", "Claim.png"]
    
    for image_name in test_images:
        print(f"\nTest nhận diện: {image_name}")
        
        image_path = os.path.join(image_dir, image_name)
        if not os.path.exists(image_path):
            print(f"❌ Không tìm thấy file: {image_name}")
            continue
            
        try:
            # Đọc hình ảnh mẫu
            template = cv2.imread(image_path)
            if template is None:
                print(f"❌ Không thể đọc file: {image_name}")
                continue
            
            print(f"✅ Đọc file thành công: {image_name}")
            print(f"   Kích thước: {template.shape[1]}x{template.shape[0]} pixels")
            
            # Chụp màn hình để test
            try:
                screenshot = pyautogui.screenshot()
                screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                print(f"✅ Chụp màn hình thành công: {screenshot.size}")
                
                # Test nhận diện
                result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
                locations = np.where(result >= confidence)
                
                if len(locations[0]) > 0:
                    count = len(locations[0])
                    y, x = locations[0][0], locations[1][0]
                    print(f"✅ Tìm thấy {count} vị trí khớp (độ tin cậy >= {confidence})")
                    print(f"   Vị trí đầu tiên: ({x}, {y})")
                else:
                    print(f"❌ Không tìm thấy hình ảnh trên màn hình (độ tin cậy >= {confidence})")
                    
            except Exception as e:
                print(f"❌ Lỗi khi chụp màn hình: {e}")
                
        except Exception as e:
            print(f"❌ Lỗi khi xử lý {image_name}: {e}")
    
    print("\n" + "=" * 40)
    print("Demo test hoàn thành!")
    print("Nếu tất cả hình ảnh đều được đọc thành công,")
    print("ứng dụng auto-clicker sẽ hoạt động bình thường.")

def show_image_info():
    """Hiển thị thông tin các hình ảnh"""
    print("\nThông tin các hình ảnh:")
    print("-" * 30)
    
    image_dir = "image"
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(image_dir, filename)
            try:
                with Image.open(filepath) as img:
                    print(f"{filename}: {img.size[0]}x{img.size[1]} px, {img.mode}")
            except Exception as e:
                print(f"{filename}: Lỗi đọc file - {e}")

if __name__ == "__main__":
    try:
        show_image_info()
        test_image_recognition()
    except KeyboardInterrupt:
        print("\nDừng test...")
    except Exception as e:
        print(f"Lỗi: {e}")
        print("\nVui lòng cài đặt các thư viện cần thiết:")
        print("pip install -r requirements.txt")
