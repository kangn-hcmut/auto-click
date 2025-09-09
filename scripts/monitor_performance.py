#!/usr/bin/env python3
"""
Monitor hiệu suất cho Auto Clicker v.0.3
"""

import time
import threading
import json
import os
import sys
from datetime import datetime

try:
    import psutil
except ImportError:
    print("⚠️  Cần cài đặt psutil: pip install psutil")
    sys.exit(1)

class PerformanceMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.stats = {
            "cpu_usage": [],
            "memory_usage": [],
            "disk_usage": [],
            "click_count": 0,
            "runtime": 0,
            "start_time": None,
            "mode": "unknown"
        }
        
    def start_monitoring(self, mode="unknown"):
        """Bắt đầu monitor"""
        self.is_monitoring = True
        self.start_time = time.time()
        self.stats["start_time"] = datetime.now().isoformat()
        self.stats["mode"] = mode
        
        # Reset stats
        self.stats["cpu_usage"] = []
        self.stats["memory_usage"] = []
        self.stats["disk_usage"] = []
        
        thread = threading.Thread(target=self._monitor_loop, daemon=True)
        thread.start()
        print(f"🔍 Performance monitoring started for {mode} mode...")
        
    def stop_monitoring(self):
        """Dừng monitor"""
        self.is_monitoring = False
        self.stats["runtime"] = time.time() - self.start_time if self.start_time else 0
        print("🔍 Performance monitoring stopped.")
        
    def _monitor_loop(self):
        """Vòng lặp monitor"""
        while self.is_monitoring:
            try:
                # CPU usage
                cpu = psutil.cpu_percent(interval=0.1)
                self.stats["cpu_usage"].append(cpu)
                
                # Memory usage
                memory = psutil.virtual_memory().percent
                self.stats["memory_usage"].append(memory)
                
                # Disk usage (current directory)
                disk = psutil.disk_usage('.').percent
                self.stats["disk_usage"].append(disk)
                
                time.sleep(1)
            except Exception as e:
                print(f"❌ Monitor error: {e}")
                break
    
    def increment_click(self):
        """Tăng số lần click"""
        self.stats["click_count"] += 1
        
    def get_stats(self):
        """Lấy thống kê"""
        if self.start_time:
            self.stats["runtime"] = time.time() - self.start_time
        return self.stats.copy()
        
    def print_stats(self):
        """In thống kê real-time"""
        stats = self.get_stats()
        
        print(f"\n{'='*50}")
        print(f"🔍 Performance Stats - {stats['mode'].upper()} Mode")
        print(f"{'='*50}")
        
        # Basic info
        print(f"⏱️  Runtime: {stats['runtime']:.1f} seconds")
        print(f"🖱️  Total clicks: {stats['click_count']}")
        
        # CPU stats
        if stats["cpu_usage"]:
            cpu_avg = sum(stats['cpu_usage']) / len(stats['cpu_usage'])
            cpu_max = max(stats['cpu_usage'])
            cpu_current = stats['cpu_usage'][-1] if stats['cpu_usage'] else 0
            print(f"🖥️  CPU - Current: {cpu_current:.1f}% | Avg: {cpu_avg:.1f}% | Max: {cpu_max:.1f}%")
            
        # Memory stats  
        if stats["memory_usage"]:
            mem_avg = sum(stats['memory_usage']) / len(stats['memory_usage'])
            mem_max = max(stats['memory_usage'])
            mem_current = stats['memory_usage'][-1] if stats['memory_usage'] else 0
            print(f"🧠 RAM - Current: {mem_current:.1f}% | Avg: {mem_avg:.1f}% | Max: {mem_max:.1f}%")
        
        # Performance rating
        if stats["cpu_usage"] and stats["memory_usage"]:
            cpu_avg = sum(stats['cpu_usage']) / len(stats['cpu_usage'])
            mem_avg = sum(stats['memory_usage']) / len(stats['memory_usage'])
            
            if cpu_avg < 10 and mem_avg < 50:
                rating = "🟢 Excellent"
            elif cpu_avg < 25 and mem_avg < 70:
                rating = "🟡 Good"  
            elif cpu_avg < 50 and mem_avg < 85:
                rating = "🟠 Fair"
            else:
                rating = "🔴 Poor"
                
            print(f"📊 Performance: {rating}")
        
        # Efficiency (clicks per minute)
        if stats["runtime"] > 0:
            cpm = (stats["click_count"] / stats["runtime"]) * 60
            print(f"⚡ Efficiency: {cpm:.1f} clicks/minute")
            
    def save_stats(self, filename=None):
        """Lưu thống kê vào file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_log_{timestamp}.json"
            
        stats = self.get_stats()
        
        try:
            with open(filename, 'w') as f:
                json.dump(stats, f, indent=2)
            print(f"📄 Stats saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving stats: {e}")
            
    def load_and_compare(self, filename):
        """Load và so sánh với log cũ"""
        try:
            with open(filename, 'r') as f:
                old_stats = json.load(f)
                
            current_stats = self.get_stats()
            
            print(f"\n📊 Performance Comparison")
            print(f"{'='*40}")
            
            # So sánh CPU
            if old_stats.get("cpu_usage") and current_stats.get("cpu_usage"):
                old_cpu = sum(old_stats["cpu_usage"]) / len(old_stats["cpu_usage"])
                new_cpu = sum(current_stats["cpu_usage"]) / len(current_stats["cpu_usage"])
                diff = new_cpu - old_cpu
                trend = "📈" if diff > 0 else "📉" if diff < 0 else "➡️"
                print(f"CPU: {old_cpu:.1f}% → {new_cpu:.1f}% {trend} ({diff:+.1f}%)")
            
            # So sánh Memory
            if old_stats.get("memory_usage") and current_stats.get("memory_usage"):
                old_mem = sum(old_stats["memory_usage"]) / len(old_stats["memory_usage"])
                new_mem = sum(current_stats["memory_usage"]) / len(current_stats["memory_usage"])
                diff = new_mem - old_mem
                trend = "📈" if diff > 0 else "📉" if diff < 0 else "➡️"
                print(f"RAM: {old_mem:.1f}% → {new_mem:.1f}% {trend} ({diff:+.1f}%)")
                
            # So sánh Efficiency
            old_runtime = old_stats.get("runtime", 0)
            new_runtime = current_stats.get("runtime", 0)
            if old_runtime > 0 and new_runtime > 0:
                old_cpm = (old_stats.get("click_count", 0) / old_runtime) * 60
                new_cpm = (current_stats.get("click_count", 0) / new_runtime) * 60
                diff = new_cpm - old_cpm
                trend = "📈" if diff > 0 else "📉" if diff < 0 else "➡️"
                print(f"Efficiency: {old_cpm:.1f} → {new_cpm:.1f} clicks/min {trend} ({diff:+.1f})")
                
        except Exception as e:
            print(f"❌ Error loading comparison file: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor hiệu suất Auto Clicker v.0.3')
    parser.add_argument('--mode', choices=['normal', 'starfall'], default='auto',
                       help='Chế độ monitoring')
    parser.add_argument('--interval', type=int, default=5,
                       help='Interval update stats (seconds)')
    parser.add_argument('--save', action='store_true',
                       help='Tự động save stats khi dừng')
    parser.add_argument('--compare', type=str,
                       help='So sánh với file log cũ')
    
    args = parser.parse_args()
    
    monitor = PerformanceMonitor()
    
    # Detect mode if auto
    mode = args.mode
    if mode == 'auto':
        if os.path.exists('../config/starfall_config.json'):
            mode = 'starfall'
        else:
            mode = 'normal'
    
    monitor.start_monitoring(mode)
    
    try:
        print(f"🔍 Monitor đang chạy cho {mode.upper()} mode...")
        print(f"📊 Update interval: {args.interval} seconds")
        print("📝 Nhấn Ctrl+C để dừng và xem tổng kết")
        
        while True:
            time.sleep(args.interval)
            monitor.print_stats()
            
    except KeyboardInterrupt:
        print("\n🛑 Dừng monitoring...")
        monitor.stop_monitoring()
        
        # Print final stats
        print("\n" + "="*50)
        print("📊 FINAL PERFORMANCE REPORT")
        print("="*50)
        monitor.print_stats()
        
        # Save if requested
        if args.save:
            monitor.save_stats()
            
        # Compare if requested
        if args.compare:
            monitor.load_and_compare(args.compare)
            
        print("\n✅ Monitor hoàn thành!")

if __name__ == "__main__":
    main()
