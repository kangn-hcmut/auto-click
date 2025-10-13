#!/usr/bin/env python3
"""
Tool test khả năng nhận diện hình ảnh trên các độ phân giải khác nhau
"""

import os
import sys
import cv2
import numpy as np
import pyautogui
import tkinter as tk
from PIL import Image, ImageTk

def get_screen_info():
    """Lấy thông tin màn hình"""
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    
    aspect_ratio = screen_width / screen_height
    
    # Classify screen type
    if abs(aspect_ratio - 16/9) < 0.1:
        aspect_type = "16:9"
    elif abs(aspect_ratio - 16/10) < 0.1:
        aspect_type = "16:10"
    elif abs(aspect_ratio - 4/3) < 0.1:
        aspect_type = "4:3"
    else:
        aspect_type = f"{aspect_ratio:.2f}:1"
    
    # Estimate screen size
    if screen_width <= 1366:
        size_category = "Small (≤13.3\")"
    elif screen_width <= 1920:
        size_category = "Medium (14-15.6\")"
    else:
        size_category = "Large (≥17\")"
    
    return {
        'width': screen_width,
        'height': screen_height,
        'aspect_ratio': aspect_ratio,
        'aspect_type': aspect_type,
        'size_category': size_category
    }

def test_multi_scale_detection(image_name, confidence=0.8):
    """Test multi-scale detection cho một hình ảnh"""
    image_path = os.path.join("image", image_name)
    if not os.path.exists(image_path):
        print(f"❌ Không tìm thấy {image_name}")
        return None
    
    print(f"🔍 Testing detection cho {image_name}...")
    
    # Chụp màn hình
    screenshot = pyautogui.screenshot()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Đọc template
    template = cv2.imread(image_path)
    if template is None:
        print(f"❌ Không thể đọc {image_name}")
        return None
    
    print(f"📏 Template size: {template.shape[1]}x{template.shape[0]}")
    
    # Test multiple scales
    scales = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    results = []
    
    for scale in scales:
        # Resize template
        if scale != 1.0:
            new_width = int(template.shape[1] * scale)
            new_height = int(template.shape[0] * scale)
            
            if new_width < 10 or new_height < 10:
                continue
            if new_width > screenshot_cv.shape[1] or new_height > screenshot_cv.shape[0]:
                continue
                
            scaled_template = cv2.resize(template, (new_width, new_height))
        else:
            scaled_template = template
        
        # Template matching
        result = cv2.matchTemplate(screenshot_cv, scaled_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        results.append({
            'scale': scale,
            'confidence': max_val,
            'location': max_loc,
            'template_size': (scaled_template.shape[1], scaled_template.shape[0])
        })
        
        status = "✅" if max_val >= confidence else "❌"
        print(f"  Scale {scale:.2f}: {status} confidence={max_val:.3f} at {max_loc} (size: {scaled_template.shape[1]}x{scaled_template.shape[0]})")
    
    # Tìm kết quả tốt nhất
    best_result = max(results, key=lambda x: x['confidence'])
    print(f"🎯 Best match: scale={best_result['scale']:.2f}, confidence={best_result['confidence']:.3f}")
    
    return best_result

def test_all_images():
    """Test tất cả hình ảnh trong thư mục image"""
    print("=" * 60)
    print("TEST MULTI-SCALE IMAGE DETECTION")
    print("=" * 60)
    
    # Hiển thị thông tin màn hình
    screen_info = get_screen_info()
    print(f"📺 Màn hình: {screen_info['width']}x{screen_info['height']}")
    print(f"📐 Tỷ lệ: {screen_info['aspect_type']} ({screen_info['aspect_ratio']:.3f})")
    print(f"📱 Loại: {screen_info['size_category']}")
    print()
    
    # Lấy danh sách tất cả hình ảnh
    image_dir = "image"
    if not os.path.exists(image_dir):
        print(f"❌ Không tìm thấy thư mục {image_dir}")
        return
    
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print(f"❌ Không có hình ảnh trong thư mục {image_dir}")
        return
    
    # Test từng hình ảnh
    confidence_threshold = 0.7
    results = {}
    
    for image_file in sorted(image_files):
        print(f"\n{'='*40}")
        result = test_multi_scale_detection(image_file, confidence_threshold)
        results[image_file] = result
    
    # Tổng kết
    print(f"\n{'='*60}")
    print("TỔNG KẾT")
    print("=" * 60)
    
    detected_count = sum(1 for r in results.values() if r and r['confidence'] >= confidence_threshold)
    total_count = len(results)
    
    print(f"📊 Tổng số hình ảnh: {total_count}")
    print(f"✅ Phát hiện được: {detected_count}")
    print(f"❌ Không phát hiện: {total_count - detected_count}")
    print(f"📈 Tỷ lệ thành công: {(detected_count/total_count)*100:.1f}%")
    
    # Đề xuất cấu hình tối ưu
    print(f"\n🔧 ĐỀ XUẤT CẤU HỈnh:")
    
    # Tính confidence trung bình của các detection thành công
    successful_confidences = [r['confidence'] for r in results.values() 
                            if r and r['confidence'] >= confidence_threshold]
    
    if successful_confidences:
        avg_confidence = sum(successful_confidences) / len(successful_confidences)
        recommended_confidence = max(0.5, avg_confidence - 0.1)  # Thấp hơn 10% để an toàn
        print(f"   Confidence đề xuất: {recommended_confidence:.2f}")
    else:
        print(f"   Confidence đề xuất: 0.6 (do không có detection thành công)")
    
    # Screen-specific recommendations
    if screen_info['width'] <= 1366:
        print("   Màn hình nhỏ: Nên sử dụng multi-scale detection")
        print("   Đề xuất: confidence 0.6-0.7, enable rotation detection")
    elif screen_info['width'] <= 1920:
        print("   Màn hình trung bình: Cấu hình chuẩn")
        print("   Đề xuất: confidence 0.7-0.8, multi-scale khi cần")
    else:
        print("   Màn hình lớn: Có thể dùng confidence cao hơn")
        print("   Đề xuất: confidence 0.8-0.9, ít cần multi-scale")

def main():
    if len(sys.argv) > 1:
        # Test một hình ảnh cụ thể
        image_name = sys.argv[1]
        confidence = 0.8
        if len(sys.argv) > 2:
            confidence = float(sys.argv[2])
        
        screen_info = get_screen_info()
        print(f"📺 Màn hình: {screen_info['width']}x{screen_info['height']} ({screen_info['aspect_type']})")
        print()
        
        test_multi_scale_detection(image_name, confidence)
    else:
        # Test tất cả hình ảnh
        test_all_images()

if __name__ == "__main__":
    main()