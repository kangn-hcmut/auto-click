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
    
    def load_default_config(self):
        """Tải cấu hình mặc định"""
        if self.current_mode == "starfall":
            return {
                "mode": "starfall",
                "max_attempts": 20,
                "confidence": 0.7,
                "images": ["ads.png", "ads_close.png", "ads_close2.png", "ads_close3.png", "star_claim.png"],
                "cycle_delay": 10,
                "scan_interval": 1
            }
        else:
            return {
                "mode": "normal", 
                "collect_gold": True,
                "collect_gems": True,
                "confidence": 0.8,
                "images": ["gold2.png", "gold.png", "coin.png", "Gems.png", "OK.png", "ads_close.png", "ads_close2.png", "ads_close3.png", "Claim.png"],
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
        """Tìm kiếm hình ảnh trên màn hình"""
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
                
            # Tìm kiếm hình ảnh
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= confidence)
            
            if len(locations[0]) > 0:
                # Lấy vị trí đầu tiên tìm thấy
                y, x = locations[0][0], locations[1][0]
                h, w = template.shape[:2]
                center_x = x + w // 2
                center_y = y + h // 2
                self.log_message(f"Tìm thấy {image_name} tại ({center_x}, {center_y})")
                return (center_x, center_y)
            else:
                self.log_message(f"Không tìm thấy {image_name} trên màn hình")
                return None
                
        except Exception as e:
            self.log_message(f"Lỗi khi tìm kiếm {image_name}: {str(e)}")
            return None
    
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
            gold2_pos = self.find_image_on_screen("gold2.png", confidence)
            if gold2_pos and self.is_running:
                self.log_message(f"Phát hiện gold2.png lần {collected_count + 1}")
                self.click_at_position(gold2_pos)
                collected_count += 1
                found_something = True
                time.sleep(wait_time)
                continue
            
            gold_pos = self.find_image_on_screen("gold.png", confidence)
            if gold_pos and self.is_running:
                self.log_message(f"Phát hiện gold.png lần {collected_count + 1}")
                self.click_at_position(gold_pos)
                collected_count += 1
                found_something = True
                time.sleep(wait_time)
                continue
                
            coin_pos = self.find_image_on_screen("coin.png", confidence)
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

    def close_popup_if_exists(self, confidence, wait_time):
        """Đóng popup nếu tìm thấy nút close_pop_up"""
        close_pop_up_pos = self.find_image_on_screen("close_pop_up.png", confidence)
        if close_pop_up_pos and self.is_running:
            self.log_message("Phát hiện popup close_pop_up.png, đang đóng...")
            self.click_at_position(close_pop_up_pos)
            time.sleep(wait_time)
            return True
        return False

    def starfall_workflow(self, confidence):
        """Workflow cho Starfall Mode - vòng lặp duy nhất quét tất cả trạng thái liên tục"""
        self.log_message("🔄 Bắt đầu Starfall Mode workflow - quét liên tục...")
        
        scan_count = 0
        max_scan_time = 180  # Maximum 3 minutes for full cycle
        workflow_complete = False
        
        # Đầu tiên check popup nếu có
        self.close_popup_if_exists(confidence, 1)
        
        while scan_count < max_scan_time and self.is_running:
            # Priority 1: Check for star_claim button (final step)
            star_claim_pos = self.find_image_on_screen("star_claim.png", confidence)
            if star_claim_pos:
                self.log_message(f"🎯 Tìm thấy nút star_claim sau {scan_count}s!")
                self.click_at_position(star_claim_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                self.log_message("✅ Hoàn thành 1 chu kì Starfall!")
                workflow_complete = True
                break
            
            # Priority 2: Check for ads_close buttons (may appear before star_claim)
            ads_close_pos = self.find_image_on_screen("ads_close.png", confidence)
            if ads_close_pos:
                self.log_message(f"🎯 Tìm thấy nút ads_close sau {scan_count}s!")
                self.click_at_position(ads_close_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                time.sleep(1)
                scan_count += 1
                continue
            
            ads_close2_pos = self.find_image_on_screen("ads_close2.png", confidence)
            if ads_close2_pos:
                self.log_message(f"🎯 Tìm thấy nút ads_close2 sau {scan_count}s!")
                self.click_at_position(ads_close2_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                time.sleep(1)
                scan_count += 1
                continue
            
            ads_close3_pos = self.find_image_on_screen("ads_close3.png", confidence)
            if ads_close3_pos:
                self.log_message(f"🎯 Tìm thấy nút ads_close3 sau {scan_count}s!")
                self.click_at_position(ads_close3_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                time.sleep(1)
                scan_count += 1
                continue
            
            # Priority 3: Check for ads button
            ads_pos = self.find_image_on_screen("ads.png", confidence)
            if ads_pos:
                self.log_message(f"🎯 Tìm thấy nút ads sau {scan_count}s!")
                self.click_at_position(ads_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                time.sleep(1)
                scan_count += 1
                continue
            
            # Priority 4: Check for popups to close
            if self.close_popup_if_exists(confidence, 1):
                scan_count += 1
                continue
            
            # Progress logging every 10 seconds
            if scan_count > 0 and scan_count % 10 == 0:
                self.log_message(f"⏳ Đã quét {scan_count}s, tiếp tục tìm kiếm...")
            
            scan_count += 1
            time.sleep(1)  # Wait 1 second before next scan
        
        if not workflow_complete:
            self.log_message(f"❌ Không hoàn thành workflow sau {scan_count}s")
            return False
        
        return True
    
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
        """Workflow cho Normal Mode - vòng lặp duy nhất quét tất cả trạng thái liên tục"""
        self.log_message("🔄 Bắt đầu Normal Mode workflow - quét liên tục...")
        
        scan_count = 0
        max_scan_time = 60  # Maximum 1 minute for full cycle
        workflow_complete = False
        
        while scan_count < max_scan_time and self.is_running:
            # Priority 1: Check for Claim button (final step)
            claim_pos = self.find_image_on_screen("Claim.png", confidence)
            if claim_pos:
                self.log_message(f"🎯 Tìm thấy nút Claim sau {scan_count}s!")
                self.click_at_position(claim_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                self.log_message("✅ Hoàn thành 1 chu kì Normal Mode!")
                workflow_complete = True
                break
            
            # Priority 2: Check for ads_close buttons (may appear before Claim)
            ads_close_pos = self.find_image_on_screen("ads_close.png", confidence)
            if ads_close_pos:
                self.log_message(f"🎯 Tìm thấy nút ads_close sau {scan_count}s!")
                self.click_at_position(ads_close_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                time.sleep(wait_time)
                scan_count += 1
                continue
            
            ads_close2_pos = self.find_image_on_screen("ads_close2.png", confidence)
            if ads_close2_pos:
                self.log_message(f"🎯 Tìm thấy nút ads_close2 sau {scan_count}s!")
                self.click_at_position(ads_close2_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                time.sleep(wait_time)
                scan_count += 1
                continue
            
            ads_close3_pos = self.find_image_on_screen("ads_close3.png", confidence)
            if ads_close3_pos:
                self.log_message(f"🎯 Tìm thấy nút ads_close3 sau {scan_count}s!")
                self.click_at_position(ads_close3_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                time.sleep(wait_time)
                scan_count += 1
                continue
            
            # Priority 3: Check for OK popup
            ok_pos = self.find_image_on_screen("OK.png", confidence)
            if ok_pos:
                self.log_message(f"🎯 Tìm thấy popup OK sau {scan_count}s!")
                self.click_at_position(ok_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                time.sleep(wait_time)
                scan_count += 1
                continue
            
            # Priority 4: Check for Gems button
            gems_pos = self.find_image_on_screen("Gems.png", confidence)
            if gems_pos:
                self.log_message(f"🎯 Tìm thấy Gems.png sau {scan_count}s!")
                self.click_at_position(gems_pos)
                self.click_count += 1
                self.click_count_var.set(str(self.click_count))
                time.sleep(wait_time)
                scan_count += 1
                continue
            
            # Priority 5: Check for popups to close
            if self.close_popup_if_exists(confidence, wait_time):
                scan_count += 1
                continue

            
            
            # Progress logging every 10 seconds
            if scan_count > 0 and scan_count % 10 == 0:
                self.log_message(f"⏳ Đã quét {scan_count}s, tiếp tục tìm kiếm...")
            
            scan_count += 1
            time.sleep(1)  # Wait 1 second before next scan
            self.close_popup_if_exists(confidence, wait_time)

        
        if not workflow_complete:
            self.log_message(f"❌ Không hoàn thành workflow sau {scan_count}s")
            return False
        
        return True
    
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
