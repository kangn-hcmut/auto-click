import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import numpy as np
import pyautogui
import threading
import time
from PIL import Image, ImageTk
import os

class AutoClickerApp:
    def __init__(self, root, mode=None, config=None, debug=False):
        self.root = root
        self.root.title("Auto Clicker v.0.3 - Game Bot")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        
        # Trạng thái ứng dụng
        self.is_running = False
        self.click_count = 0
        self.status = "Đã dừng"
        self.current_mode = mode or "normal"
        self.debug_mode = debug
        
        # Cấu hình
        self.config = config or self.load_default_config()
        
        # Đường dẫn thư mục hình ảnh
        self.image_dir = "image"
        
        # Thiết lập giao diện
        self.setup_ui()
        
        # Cấu hình pyautogui
        pyautogui.FAILSAFE = True  # Di chuyển chuột tới góc trái trên để dừng khẩn cấp
        pyautogui.PAUSE = 0.5  # Tạm dừng giữa các lệnh
        
        # Log thông tin khởi chạy
        self.log_message(f"Khởi chạy Auto Clicker v.0.3")
        self.log_message(f"Chế độ hiện tại: {self.current_mode.title()} Mode")
        if self.debug_mode:
            self.log_message("Chế độ debug: BẬT")
        
        # Detect screen info
        self.detect_screen_info()
    
    def detect_screen_info(self):
        """Phát hiện thông tin màn hình và điều chỉnh cấu hình"""
        try:
            import tkinter as tk
            root = tk.Tk()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            root.destroy()
            
            # Tính tỷ lệ màn hình
            aspect_ratio = screen_width / screen_height
            screen_diagonal = (screen_width**2 + screen_height**2)**0.5
            
            # Classify screen type
            if abs(aspect_ratio - 16/9) < 0.1:
                aspect_type = "16:9"
            elif abs(aspect_ratio - 16/10) < 0.1:
                aspect_type = "16:10"
            elif abs(aspect_ratio - 4/3) < 0.1:
                aspect_type = "4:3"
            else:
                aspect_type = f"{aspect_ratio:.2f}:1"
            
            # Estimate screen size (rough)
            if screen_width <= 1366:
                size_category = "Small (≤13.3\")"
                confidence_adjust = 0.1  # Lower confidence for small screens
            elif screen_width <= 1920:
                size_category = "Medium (14-15.6\")"
                confidence_adjust = 0.0  # Standard confidence
            else:
                size_category = "Large (≥17\")"
                confidence_adjust = -0.05  # Slightly higher confidence for large screens
            
            # Adjust confidence based on screen
            adjusted_confidence = float(self.confidence_var.get()) + confidence_adjust
            adjusted_confidence = max(0.5, min(0.95, adjusted_confidence))  # Clamp between 0.5-0.95
            
            self.log_message(f"📺 Màn hình: {screen_width}x{screen_height} ({aspect_type}) - {size_category}")
            self.log_message(f"🎯 Confidence điều chỉnh: {float(self.confidence_var.get()):.2f} → {adjusted_confidence:.2f}")
            
            # Update confidence if significant change
            if abs(adjusted_confidence - float(self.confidence_var.get())) > 0.05:
                self.confidence_var.set(f"{adjusted_confidence:.2f}")
                self.log_message(f"✅ Đã tự động điều chỉnh confidence cho màn hình này")
            
        except Exception as e:
            self.log_message(f"⚠️ Không thể detect screen info: {e}")
    
    def load_default_config(self):
        """Tải cấu hình mặc định"""
        if self.current_mode == "starfall":
            return {
                "mode": "starfall",
                "max_attempts": 20,
                "confidence": 0.7,
                "images": ["ads.png", "star_claim.png"],
                "cycle_delay": 10,
                "scan_interval": 1
            }
        else:
            return {
                "mode": "normal", 
                "collect_gold": True,
                "collect_gems": True,
                "confidence": 0.8,
                "images": ["gold2.png", "gold.png", "coin.png", "Gems.png", "OK.png", "Claim.png"],
                "cycle_delay": 5,
                "scan_interval": 1
            }
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="Auto Clicker v.0.3 - Game Bot", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame chế độ
        mode_frame = ttk.LabelFrame(main_frame, text="Chế độ hoạt động", padding="10")
        mode_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Radio buttons cho chế độ
        self.mode_var = tk.StringVar(value=self.current_mode)
        
        normal_radio = ttk.Radiobutton(mode_frame, text="Normal Mode (Thu lượm + Gems)", 
                                      variable=self.mode_var, value="normal",
                                      command=self.on_mode_change)
        normal_radio.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        starfall_radio = ttk.Radiobutton(mode_frame, text="Starfall Mode (Xem ads)", 
                                        variable=self.mode_var, value="starfall",
                                        command=self.on_mode_change)
        starfall_radio.grid(row=0, column=1, sticky=tk.W)
        
        # Frame thông tin
        info_frame = ttk.LabelFrame(main_frame, text="Thông tin", padding="10")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Số lần click
        ttk.Label(info_frame, text="Số lần click:").grid(row=0, column=0, sticky=tk.W)
        self.click_count_var = tk.StringVar(value="0")
        self.click_count_label = ttk.Label(info_frame, textvariable=self.click_count_var, 
                                          font=("Arial", 12, "bold"), foreground="blue")
        self.click_count_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Trạng thái
        ttk.Label(info_frame, text="Trạng thái:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.status_var = tk.StringVar(value=self.status)
        self.status_label = ttk.Label(info_frame, textvariable=self.status_var, 
                                     font=("Arial", 12, "bold"), foreground="red")
        self.status_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Chế độ hiện tại
        ttk.Label(info_frame, text="Chế độ:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.current_mode_var = tk.StringVar(value=self.current_mode.title())
        mode_label = ttk.Label(info_frame, textvariable=self.current_mode_var, 
                              font=("Arial", 12, "bold"), foreground="purple")
        mode_label.grid(row=0, column=3, sticky=tk.W, padx=(10, 0))
        
        # Frame điều khiển
        control_frame = ttk.LabelFrame(main_frame, text="Điều khiển", padding="10")
        control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Nút Start
        self.start_button = ttk.Button(control_frame, text="Bắt đầu", 
                                      command=self.start_clicking)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        # Nút Stop
        self.stop_button = ttk.Button(control_frame, text="Dừng lại", 
                                     command=self.stop_clicking, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        # Nút Reset
        self.reset_button = ttk.Button(control_frame, text="Reset", 
                                      command=self.reset_counter)
        self.reset_button.grid(row=0, column=2, padx=(0, 10))
        
        # Nút Save Config
        self.save_config_button = ttk.Button(control_frame, text="Lưu cấu hình", 
                                           command=self.save_current_config)
        self.save_config_button.grid(row=0, column=3)
        
        # Frame cấu hình
        config_frame = ttk.LabelFrame(main_frame, text="Cấu hình", padding="10")
        config_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Thời gian chờ giữa các bước
        ttk.Label(config_frame, text="Thời gian chờ (giây):").grid(row=0, column=0, sticky=tk.W)
        self.wait_time_var = tk.StringVar(value="2")
        wait_time_entry = ttk.Entry(config_frame, textvariable=self.wait_time_var, width=10)
        wait_time_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Độ chính xác tìm kiếm hình ảnh
        ttk.Label(config_frame, text="Độ chính xác:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.confidence_var = tk.StringVar(value=str(self.config.get('confidence', 0.8)))
        confidence_entry = ttk.Entry(config_frame, textvariable=self.confidence_var, width=10)
        confidence_entry.grid(row=0, column=3, sticky=tk.W, padx=(10, 0))
        
        # Chu kì delay
        ttk.Label(config_frame, text="Nghỉ giữa chu kì (s):").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.cycle_delay_var = tk.StringVar(value=str(self.config.get('cycle_delay', 5)))
        cycle_delay_entry = ttk.Entry(config_frame, textvariable=self.cycle_delay_var, width=10)
        cycle_delay_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Text log
        log_frame = ttk.LabelFrame(main_frame, text="Log hoạt động", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Text widget với scrollbar
        self.log_text = tk.Text(log_frame, height=10, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Cấu hình grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(5, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def on_mode_change(self):
        """Xử lý khi thay đổi chế độ"""
        new_mode = self.mode_var.get()
        if new_mode != self.current_mode:
            self.current_mode = new_mode
            self.current_mode_var.set(new_mode.title())
            self.config = self.load_default_config()
            self.confidence_var.set(str(self.config.get('confidence', 0.8)))
            self.cycle_delay_var.set(str(self.config.get('cycle_delay', 5)))
            self.log_message(f"Đã chuyển sang {new_mode.title()} Mode")
    
    def save_current_config(self):
        """Lưu cấu hình hiện tại"""
        import json
        config_dir = "config"
        os.makedirs(config_dir, exist_ok=True)
        
        # Cập nhật config với giá trị hiện tại
        self.config['confidence'] = float(self.confidence_var.get())
        self.config['cycle_delay'] = int(self.cycle_delay_var.get())
        
        config_file = os.path.join(config_dir, f"{self.current_mode}_config.json")
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.log_message(f"Đã lưu cấu hình vào {config_file}")
        except Exception as e:
            self.log_message(f"Lỗi khi lưu cấu hình: {e}")

    def log_message(self, message):
        """Thêm thông điệp vào log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def find_image_on_screen(self, image_name, confidence=0.8):
        """Tìm kiếm hình ảnh trên màn hình với multi-scale detection"""
        try:
            image_path = os.path.join(self.image_dir, image_name)
            if not os.path.exists(image_path):
                self.log_message(f"Không tìm thấy file hình ảnh: {image_name}")
                return None
                
            # Chụp màn hình
            screenshot = pyautogui.screenshot()
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Đọc hình ảnh mẫu
            template = cv2.imread(image_path)
            if template is None:
                self.log_message(f"Không thể đọc file hình ảnh: {image_name}")
                return None
                
            # Multi-scale template matching cho các độ phân giải khác nhau
            # Scales để test: 0.5x, 0.75x, 1.0x, 1.25x, 1.5x, 2.0x
            scales = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
            best_match = None
            best_confidence = 0
            best_location = None
            best_scale = 1.0
            
            for scale in scales:
                # Resize template theo scale
                if scale != 1.0:
                    new_width = int(template.shape[1] * scale)
                    new_height = int(template.shape[0] * scale)
                    
                    # Bỏ qua nếu template quá lớn hoặc quá nhỏ
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
                
                # Lưu kết quả tốt nhất
                if max_val > best_confidence and max_val >= confidence:
                    best_confidence = max_val
                    best_location = max_loc
                    best_scale = scale
                    h, w = scaled_template.shape[:2]
                    best_match = (w, h)
                    
                if self.debug_mode:
                    self.log_message(f"Scale {scale:.2f}: confidence={max_val:.3f} at {max_loc}")
            
            if best_location is not None:
                x, y = best_location
                w, h = best_match
                center_x = x + w // 2
                center_y = y + h // 2
                
                scale_info = f" (scale={best_scale:.2f})" if best_scale != 1.0 else ""
                self.log_message(f"Tìm thấy {image_name} tại ({center_x}, {center_y}) với confidence={best_confidence:.3f}{scale_info}")
                return (center_x, center_y)
            else:
                self.log_message(f"Không tìm thấy {image_name} trên màn hình (đã thử {len(scales)} scales)")
                return None
                
        except Exception as e:
            self.log_message(f"Lỗi khi tìm kiếm {image_name}: {str(e)}")
            return None
    
    def find_image_with_rotation(self, image_name, confidence=0.8):
        """Tìm kiếm hình ảnh với khả năng xoay nhẹ (cho trường hợp màn hình bị nghiêng)"""
        try:
            image_path = os.path.join(self.image_dir, image_name)
            if not os.path.exists(image_path):
                return None
                
            screenshot = pyautogui.screenshot()
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            template = cv2.imread(image_path)
            
            if template is None:
                return None
            
            best_match = None
            best_confidence = 0
            
            # Test với các góc xoay nhẹ: -5°, 0°, +5°
            rotation_angles = [-5, 0, 5]
            scales = [0.8, 0.9, 1.0, 1.1, 1.2]
            
            for angle in rotation_angles:
                for scale in scales:
                    if not self.is_running:
                        break
                        
                    # Xoay và scale template
                    center = (template.shape[1]//2, template.shape[0]//2)
                    
                    # Scale first
                    if scale != 1.0:
                        new_w = int(template.shape[1] * scale)
                        new_h = int(template.shape[0] * scale)
                        if new_w < 10 or new_h < 10 or new_w > screenshot_cv.shape[1] or new_h > screenshot_cv.shape[0]:
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
                    
                    # Template matching
                    result = cv2.matchTemplate(screenshot_cv, rotated_template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    
                    if max_val > best_confidence and max_val >= confidence:
                        best_confidence = max_val
                        h, w = rotated_template.shape[:2]
                        center_x = max_loc[0] + w // 2
                        center_y = max_loc[1] + h // 2
                        best_match = (center_x, center_y, scale, angle)
                        
                        if self.debug_mode:
                            self.log_message(f"Better match: scale={scale:.2f}, angle={angle}°, conf={max_val:.3f}")
            
            if best_match:
                x, y, scale, angle = best_match
                transform_info = ""
                if scale != 1.0:
                    transform_info += f" scale={scale:.2f}"
                if angle != 0:
                    transform_info += f" angle={angle}°"
                    
                self.log_message(f"Tìm thấy {image_name} tại ({x}, {y}) với confidence={best_confidence:.3f}{transform_info}")
                return (x, y)
            else:
                self.log_message(f"Không tìm thấy {image_name} (đã thử multi-scale + rotation)")
                return None
                
        except Exception as e:
            self.log_message(f"Lỗi multi-scale detection {image_name}: {str(e)}")
            return None
    
    def adaptive_find_image(self, image_name, confidence=0.8, use_rotation=False):
        """Tìm kiếm thích ứng: thử standard trước, sau đó multi-scale nếu cần"""
        # Thử standard detection trước (nhanh hơn)
        result = self.find_image_on_screen(image_name, confidence)
        
        # Nếu không tìm thấy và confidence cao, thử giảm confidence
        if result is None and confidence > 0.6:
            lower_confidence = confidence - 0.1
            result = self.find_image_on_screen(image_name, lower_confidence)
            if result:
                self.log_message(f"📉 Tìm thấy với confidence thấp hơn: {lower_confidence:.2f}")
        
        # Nếu vẫn không tìm thấy và yêu cầu rotation, thử multi-scale + rotation
        if result is None and use_rotation:
            self.log_message(f"🔄 Thử multi-scale + rotation cho {image_name}...")
            result = self.find_image_with_rotation(image_name, confidence)
        
        return result
    
    def click_at_position(self, position):
        """Click tại vị trí được chỉ định"""
        try:
            x, y = position
            pyautogui.click(x, y)
            self.log_message(f"Đã click tại vị trí ({x}, {y})")
            return True
        except Exception as e:
            self.log_message(f"Lỗi khi click: {str(e)}")
            return False
    
    def collect_all_gold_coins(self, confidence, wait_time):
        """Thu lượm tất cả gold và coin có thể tìm thấy"""
        collected_count = 0
        max_attempts = 10  # Giới hạn số lần thử để tránh vòng lặp vô tận
        
        self.log_message("Bắt đầu thu lượm gold/coin...")
        
        for attempt in range(max_attempts):
            if not self.is_running:
                break
                
            found_something = False
            
            # Tìm kiếm các loại gold/coin theo thứ tự ưu tiên
            gold2_pos = self.adaptive_find_image("gold2.png", confidence)
            if gold2_pos and self.is_running:
                self.log_message(f"Phát hiện gold2.png lần {collected_count + 1}")
                self.click_at_position(gold2_pos)
                collected_count += 1
                found_something = True
                time.sleep(wait_time)
                continue
            
            gold_pos = self.adaptive_find_image("gold.png", confidence)
            if gold_pos and self.is_running:
                self.log_message(f"Phát hiện gold.png lần {collected_count + 1}")
                self.click_at_position(gold_pos)
                collected_count += 1
                found_something = True
                time.sleep(wait_time)
                continue
                
            coin_pos = self.adaptive_find_image("coin.png", confidence)
            if coin_pos and self.is_running:
                self.log_message(f"Phát hiện coin.png lần {collected_count + 1}")
                self.click_at_position(coin_pos)
                collected_count += 1
                found_something = True
                time.sleep(wait_time)
                continue
            
            # Nếu không tìm thấy gì thì dừng lại
            if not found_something:
                break
        
        if collected_count > 0:
            self.log_message(f"Đã thu lượm {collected_count} gold/coin!")
        else:
            self.log_message("Không tìm thấy gold/coin nào để thu lượm")
        
        return collected_count
    
    def starfall_workflow(self, confidence):
        """Workflow cho Starfall Mode - continuously scan for ads.png and Claim.png"""
        self.log_message("Bắt đầu Starfall Mode workflow...")
        
        # Step 1: Tìm và click vào nút ads
        self.log_message("Bước 1: Tìm kiếm nút xem ads...")
        ads_pos = self.adaptive_find_image("ads.png", confidence, use_rotation=True)
        
        if not ads_pos:
            self.log_message("Không tìm thấy nút ads.png, thử lại sau...")
            return False
        
        # Click vào nút ads
        self.click_at_position(ads_pos)
        self.click_count += 1
        self.click_count_var.set(str(self.click_count))
        
        # Step 2: Continuously scan for star_claim button (ads duration varies: 5s, 15s, 30s, 40s, 45s, etc.)
        self.log_message("Bước 2: Quét màn hình liên tục để tìm nút star_claim...")
        scan_count = 0
        max_scan_time = 120  # Maximum 2 minutes scanning
        
        for scan_count in range(max_scan_time):
            if not self.is_running:
                return False
            
            # Scan for star_claim button every second
            claim_pos = self.adaptive_find_image("star_claim.png", confidence, use_rotation=True)
            if claim_pos:
                self.log_message(f"🎯 Tìm thấy nút star_claim sau {scan_count}s!")
                self.click_at_position(claim_pos)
                self.log_message("✅ Hoàn thành 1 chu kì Starfall!")
                return True
            
            # Also check if ads button appears again (in case previous ads failed)
            ads_pos = self.adaptive_find_image("ads.png", confidence)
            if ads_pos and scan_count > 10:  # Only check after 10s to avoid immediate re-click
                self.log_message("🔄 Phát hiện ads.png lại, có thể ads trước đó thất bại")
                self.click_at_position(ads_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                scan_count = 0  # Reset scan counter
            
            # Progress logging every 10 seconds
            if scan_count > 0 and scan_count % 10 == 0:
                self.log_message(f"⏳ Đã quét {scan_count}s, tiếp tục tìm star_claim...")
            
            time.sleep(1)  # Scan every 1 second
        
        self.log_message(f"❌ Không tìm thấy nút star_claim sau {max_scan_time}s")
        return False
    
    def auto_click_sequence(self):
        """Thực hiện chuỗi auto-click theo chế độ được chọn"""
        wait_time = float(self.wait_time_var.get())
        confidence = float(self.confidence_var.get())
        
        self.log_message(f"Bắt đầu {self.current_mode.title()} Mode")
        
        cycle_count = 0
        while self.is_running:
            try:
                cycle_count += 1
                self.log_message(f"--- Chu kì #{cycle_count} ---")
                
                if self.current_mode == "starfall":
                    # Starfall Mode: Continuously scan for ads and claim
                    success = self.starfall_workflow(confidence)
                    if success:
                        cycle_delay = self.config.get('cycle_delay', 10)
                        self.log_message(f"Nghỉ {cycle_delay} giây trước chu kì tiếp theo...")
                        time.sleep(cycle_delay)
                    else:
                        self.log_message("Chu kì thất bại, thử lại sau 5 giây...")
                        time.sleep(5)
                        
                else:
                    # Normal Mode: Thu lượm + Gems với continuous scanning
                    success = self.normal_workflow(confidence, wait_time)
                    if success:
                        cycle_delay = self.config.get('cycle_delay', 5)
                        self.log_message(f"Nghỉ {cycle_delay} giây trước chu kì tiếp theo...")
                        time.sleep(cycle_delay)
                    else:
                        self.log_message("Chu kì thất bại, thử lại sau 3 giây...")
                        time.sleep(3)
                
                if self.debug_mode:
                    self.log_message(f"Debug: Hoàn thành chu kì #{cycle_count}")
                    
            except Exception as e:
                self.log_message(f"Lỗi trong chu kì #{cycle_count}: {str(e)}")
                time.sleep(5)
    
    def normal_workflow(self, confidence, wait_time):
        """Workflow cho Normal Mode - thu lượm + gems + ads với continuous scanning"""
        # Step 1: Thu lượm tất cả gold/coin trước, sau đó tìm Gems.png
        self.log_message("Bước 1: Thu lượm gold/coin và tìm kiếm Gems.png...")
        
        # Thu lượm tất cả gold/coin có thể tìm thấy
        collected = self.collect_all_gold_coins(confidence, wait_time)
        
        # Sau khi thu lượm xong, tìm kiếm Gems.png
        gems_pos = self.adaptive_find_image("Gems.png", confidence, use_rotation=True)
        
        # Nếu tìm thấy Gems.png thì click và tiếp tục step 2
        if gems_pos and self.is_running:
            self.click_at_position(gems_pos)
            self.click_count += 1
            self.click_count_var.set(str(self.click_count))
            time.sleep(wait_time)
        else:
            self.log_message("Không tìm thấy Gems.png, bỏ qua step này...")
            return False
        
        # Step 2: Đợi popup và tìm OK.png
        self.log_message("Bước 2: Đợi popup và tìm kiếm OK.png...")
        for attempt in range(5):  # Thử 5 lần trong 10 giây
            if not self.is_running:
                break
            ok_pos = self.adaptive_find_image("OK.png", confidence)
            if ok_pos:
                self.click_at_position(ok_pos)
                time.sleep(wait_time)
                break
            time.sleep(2)
        else:
            self.log_message("Không tìm thấy popup OK.png, bỏ qua...")
            return False
        
        # Step 3: Continuously scan for Claim button (ads duration varies)
        self.log_message("Bước 3: Quét màn hình liên tục để tìm nút Claim...")
        scan_count = 0
        max_scan_time = 120  # Maximum 2 minutes scanning
        
        for scan_count in range(max_scan_time):
            if not self.is_running:
                break
            
            # Scan for Claim button every second
            claim_pos = self.adaptive_find_image("Claim.png", confidence, use_rotation=True)
            if claim_pos:
                self.log_message(f"🎯 Tìm thấy nút Claim sau {scan_count}s!")
                self.click_at_position(claim_pos)
                self.log_message("✅ Hoàn thành 1 chu kì Normal Mode!")
                return True
            
            # Progress logging every 10 seconds
            if scan_count > 0 and scan_count % 10 == 0:
                self.log_message(f"⏳ Đã quét {scan_count}s, tiếp tục tìm Claim...")
            
            time.sleep(1)  # Scan every 1 second
        
        self.log_message(f"❌ Không tìm thấy nút Claim sau {max_scan_time}s")
        return False
    
    def start_clicking(self):
        """Bắt đầu auto-click"""
        if not self.is_running:
            self.is_running = True
            self.status = "Đang chạy"
            self.status_var.set(self.status)
            self.status_label.configure(foreground="green")
            
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            self.log_message("Bắt đầu auto-click...")
            self.log_message("Lưu ý: Di chuyển chuột tới góc trái trên để dừng khẩn cấp")
            
            # Chạy auto-click trong thread riêng
            self.click_thread = threading.Thread(target=self.auto_click_sequence, daemon=True)
            self.click_thread.start()
    
    def stop_clicking(self):
        """Dừng auto-click"""
        self.is_running = False
        self.status = "Đã dừng"
        self.status_var.set(self.status)
        self.status_label.configure(foreground="red")
        
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        self.log_message("Đã dừng auto-click")
    
    def reset_counter(self):
        """Reset bộ đếm"""
        self.click_count = 0
        self.click_count_var.set("0")
        self.log_message("Đã reset bộ đếm")

def main():
    """Hàm main cho backward compatibility"""
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
