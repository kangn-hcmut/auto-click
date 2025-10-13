#!/usr/bin/env python3
"""
Benchmark tool để so sánh hiệu suất các phương pháp image detection
"""

import time
import cv2
import numpy as np
import pyautogui
import os

def benchmark_standard_detection(template_path, screenshot, confidence=0.8, iterations=10):
    """Benchmark standard template matching"""
    template = cv2.imread(template_path)
    if template is None:
        return None
    
    times = []
    results = []
    
    for i in range(iterations):
        start_time = time.time()
        
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= confidence)
        
        end_time = time.time()
        times.append(end_time - start_time)
        
        if len(locations[0]) > 0:
            results.append(True)
        else:
            results.append(False)
    
    avg_time = sum(times) / len(times)
    success_rate = sum(results) / len(results) * 100
    
    return {
        'method': 'Standard',
        'avg_time_ms': avg_time * 1000,
        'success_rate': success_rate,
        'iterations': iterations
    }

def benchmark_multiscale_detection(template_path, screenshot, confidence=0.8, iterations=5):
    """Benchmark multi-scale template matching"""
    template = cv2.imread(template_path)
    if template is None:
        return None
    
    scales = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    times = []
    results = []
    
    for i in range(iterations):
        start_time = time.time()
        
        found = False
        for scale in scales:
            if scale != 1.0:
                new_width = int(template.shape[1] * scale)
                new_height = int(template.shape[0] * scale)
                
                if new_width < 10 or new_height < 10:
                    continue
                if new_width > screenshot.shape[1] or new_height > screenshot.shape[0]:
                    continue
                    
                scaled_template = cv2.resize(template, (new_width, new_height))
            else:
                scaled_template = template
            
            result = cv2.matchTemplate(screenshot, scaled_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                found = True
                break
        
        end_time = time.time()
        times.append(end_time - start_time)
        results.append(found)
    
    avg_time = sum(times) / len(times)
    success_rate = sum(results) / len(results) * 100
    
    return {
        'method': 'Multi-Scale',
        'avg_time_ms': avg_time * 1000,
        'success_rate': success_rate,
        'iterations': iterations
    }

def benchmark_rotation_detection(template_path, screenshot, confidence=0.8, iterations=3):
    """Benchmark rotation + multi-scale template matching"""
    template = cv2.imread(template_path)
    if template is None:
        return None
    
    rotation_angles = [-5, 0, 5]
    scales = [0.8, 0.9, 1.0, 1.1, 1.2]
    times = []
    results = []
    
    for i in range(iterations):
        start_time = time.time()
        
        found = False
        for angle in rotation_angles:
            for scale in scales:
                # Scale first
                if scale != 1.0:
                    new_w = int(template.shape[1] * scale)
                    new_h = int(template.shape[0] * scale)
                    if new_w < 10 or new_h < 10 or new_w > screenshot.shape[1] or new_h > screenshot.shape[0]:
                        continue
                    scaled_template = cv2.resize(template, (new_w, new_h))
                else:
                    scaled_template = template
                
                # Rotate if needed
                if angle != 0:
                    center = (scaled_template.shape[1]//2, scaled_template.shape[0]//2)
                    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                    rotated_template = cv2.warpAffine(scaled_template, rotation_matrix, 
                                                    (scaled_template.shape[1], scaled_template.shape[0]))
                else:
                    rotated_template = scaled_template
                
                result = cv2.matchTemplate(screenshot, rotated_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val >= confidence:
                    found = True
                    break
            
            if found:
                break
        
        end_time = time.time()
        times.append(end_time - start_time)
        results.append(found)
    
    avg_time = sum(times) / len(times)
    success_rate = sum(results) / len(results) * 100
    
    return {
        'method': 'Multi-Scale + Rotation',
        'avg_time_ms': avg_time * 1000,
        'success_rate': success_rate,
        'iterations': iterations
    }

def run_benchmark(image_name=None):
    """Chạy benchmark cho một hoặc tất cả hình ảnh"""
    print("=" * 70)
    print("IMAGE DETECTION BENCHMARK")
    print("=" * 70)
    
    # Chụp màn hình một lần để test
    screenshot = pyautogui.screenshot()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    print(f"📺 Screen: {screenshot_cv.shape[1]}x{screenshot_cv.shape[0]}")
    print()
    
    image_dir = "image"
    
    if image_name:
        # Test một hình ảnh cụ thể
        image_files = [image_name] if os.path.exists(os.path.join(image_dir, image_name)) else []
    else:
        # Test tất cả hình ảnh
        image_files = [f for f in os.listdir(image_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))][:3]  # Limit to 3 for demo
    
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        
        print(f"🔍 Benchmarking: {image_file}")
        print("-" * 50)
        
        confidence = 0.7
        
        # Benchmark standard detection
        standard_result = benchmark_standard_detection(image_path, screenshot_cv, confidence, 10)
        
        # Benchmark multi-scale detection
        multiscale_result = benchmark_multiscale_detection(image_path, screenshot_cv, confidence, 5)
        
        # Benchmark rotation detection
        rotation_result = benchmark_rotation_detection(image_path, screenshot_cv, confidence, 3)
        
        # Display results
        results = [standard_result, multiscale_result, rotation_result]
        
        print(f"{'Method':<20} {'Time (ms)':<12} {'Success Rate':<12} {'Iterations':<12}")
        print("-" * 60)
        
        for result in results:
            if result:
                print(f"{result['method']:<20} {result['avg_time_ms']:<12.2f} {result['success_rate']:<12.1f}% {result['iterations']:<12}")
        
        # Recommendations
        print("\n💡 Recommendations:")
        
        if standard_result and standard_result['success_rate'] > 80:
            print("   ✅ Standard detection đủ tốt - dùng cho tốc độ")
        elif multiscale_result and multiscale_result['success_rate'] > 70:
            print("   🔄 Multi-scale detection - tốt cho độ chính xác")
        else:
            print("   🌟 Multi-scale + Rotation - cho độ phân giải khó")
        
        print()
    
    # Tổng kết performance
    print("=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)
    print("🚀 Standard Detection:")
    print("   + Nhanh nhất (~1-5ms)")
    print("   + Phù hợp khi hình ảnh chuẩn và màn hình ổn định")
    print("   - Có thể bỏ lỡ khi scale khác")
    print()
    print("⚖️ Multi-Scale Detection:")
    print("   + Độ chính xác cao với các độ phân giải khác nhau")
    print("   + Thời gian chấp nhận được (~10-50ms)")  
    print("   - Chậm hơn standard")
    print()
    print("🎯 Multi-Scale + Rotation:")
    print("   + Độ chính xác cao nhất")
    print("   + Xử lý được màn hình nghiêng")
    print("   - Chậm nhất (~50-200ms)")
    print("   - Nên dùng khi cần thiết")

def main():
    import sys
    
    if len(sys.argv) > 1:
        # Benchmark một hình ảnh cụ thể
        image_name = sys.argv[1]
        run_benchmark(image_name)
    else:
        # Benchmark tất cả
        run_benchmark()

if __name__ == "__main__":
    main()