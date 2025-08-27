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
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker - Game Bot")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Trạng thái ứng dụng
        self.is_running = False
        self.click_count = 0
        self.status = "Đã dừng"
        
        # Đường dẫn thư mục hình ảnh
        self.image_dir = "image"
        
        # Thiết lập giao diện
        self.setup_ui()
        
        # Cấu hình pyautogui
        pyautogui.FAILSAFE = True  # Di chuyển chuột tới góc trái trên để dừng khẩn cấp
        pyautogui.PAUSE = 0.5  # Tạm dừng giữa các lệnh
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="Auto Clicker - Game Bot", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame thông tin
        info_frame = ttk.LabelFrame(main_frame, text="Thông tin", padding="10")
        info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
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
        
        # Frame điều khiển
        control_frame = ttk.LabelFrame(main_frame, text="Điều khiển", padding="10")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Nút Start
        self.start_button = ttk.Button(control_frame, text="Bắt đầu", 
                                      command=self.start_clicking, style="Green.TButton")
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        # Nút Stop
        self.stop_button = ttk.Button(control_frame, text="Dừng lại", 
                                     command=self.stop_clicking, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        # Nút Reset
        self.reset_button = ttk.Button(control_frame, text="Reset", 
                                      command=self.reset_counter)
        self.reset_button.grid(row=0, column=2)
        
        # Frame cấu hình
        config_frame = ttk.LabelFrame(main_frame, text="Cấu hình", padding="10")
        config_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Thời gian chờ giữa các bước
        ttk.Label(config_frame, text="Thời gian chờ (giây):").grid(row=0, column=0, sticky=tk.W)
        self.wait_time_var = tk.StringVar(value="2")
        wait_time_entry = ttk.Entry(config_frame, textvariable=self.wait_time_var, width=10)
        wait_time_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Độ chính xác tìm kiếm hình ảnh
        ttk.Label(config_frame, text="Độ chính xác:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.confidence_var = tk.StringVar(value="0.8")
        confidence_entry = ttk.Entry(config_frame, textvariable=self.confidence_var, width=10)
        confidence_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Text log
        log_frame = ttk.LabelFrame(main_frame, text="Log hoạt động", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Text widget với scrollbar
        self.log_text = tk.Text(log_frame, height=8, width=60)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Cấu hình grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
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
    
    def auto_click_sequence(self):
        """Thực hiện chuỗi auto-click theo yêu cầu"""
        wait_time = float(self.wait_time_var.get())
        confidence = float(self.confidence_var.get())
        
        while self.is_running:
            try:
                # Step 1: Thu lượm tất cả gold/coin trước, sau đó tìm Gems.png
                self.log_message("Bước 1: Thu lượm gold/coin và tìm kiếm Gems.png...")
                
                # Thu lượm tất cả gold/coin có thể tìm thấy
                collected = self.collect_all_gold_coins(confidence, wait_time)
                
                # Sau khi thu lượm xong, tìm kiếm Gems.png
                gems_pos = self.find_image_on_screen("Gems.png", confidence)
                
                # Nếu tìm thấy Gems.png thì click và tiếp tục step 2
                if gems_pos and self.is_running:
                    self.click_at_position(gems_pos)
                    self.click_count += 1
                    self.click_count_var.set(str(self.click_count))
                    time.sleep(wait_time)
                else:
                    self.log_message("Không tìm thấy Gems.png, thử lại sau 3 giây...")
                    time.sleep(3)
                    continue
                
                # Step 2: Đợi popup và tìm OK.png
                self.log_message("Bước 2: Đợi popup và tìm kiếm OK.png...")
                for attempt in range(5):  # Thử 5 lần trong 10 giây
                    if not self.is_running:
                        break
                    ok_pos = self.find_image_on_screen("OK.png", confidence)
                    if ok_pos:
                        self.click_at_position(ok_pos)
                        time.sleep(wait_time)
                        break
                    time.sleep(2)
                else:
                    self.log_message("Không tìm thấy popup OK.png, bỏ qua...")
                    continue
                
                # Step 3: Chờ ads và tìm Claim.png
                self.log_message("Bước 3: Chờ ads và tìm kiếm Claim.png...")
                # Chờ ads chạy (có thể điều chỉnh thời gian này)
                ads_wait_time = 30  # 30 giây chờ ads
                for i in range(ads_wait_time):
                    if not self.is_running:
                        break
                    self.log_message(f"Chờ ads... còn {ads_wait_time - i} giây")
                    time.sleep(1)
                
                if self.is_running:
                    for attempt in range(10):  # Thử 10 lần tìm nút Claim
                        if not self.is_running:
                            break
                        claim_pos = self.find_image_on_screen("Claim.png", confidence)
                        if claim_pos:
                            self.click_at_position(claim_pos)
                            self.log_message("Hoàn thành 1 chu kì!")
                            time.sleep(wait_time)
                            break
                        time.sleep(2)
                    else:
                        self.log_message("Không tìm thấy nút Claim.png")
                
                # Nghỉ giữa các chu kì
                if self.is_running:
                    self.log_message("Nghỉ 5 giây trước chu kì tiếp theo...")
                    time.sleep(5)
                    
            except Exception as e:
                self.log_message(f"Lỗi trong chu kì auto-click: {str(e)}")
                time.sleep(5)
    
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
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
