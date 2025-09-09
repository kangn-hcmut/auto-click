# Auto Clicker - Game Bot

## Mô tả
Ứng dụng auto-click được viết bằng Python để tự động hóa việc click trong game. Ứng dụng sẽ tự động tìm kiếm và click vào các hình ảnh cụ thể theo trình tự được định sẵn.

## Các bước thực hiện
1. **Step 1**: Tìm kiếm hình ảnh `Gems.png` và click vào đó
2. **Step 2**: Đợi popup hiện lên và tìm kiếm nút `OK.png` rồi click  
3. **Step 3**: Chờ đợi ads chạy xong, tìm nút `Claim.png` rồi click để nhận thưởng

# Feature v.0.3 - Starfall Mode & Tools

## Mô tả
Chức năng này cho phép tự động xem ads để nhận starfall ticket với 2 chế độ hoạt động:
- **Normal Mode**: Thu lượm gold/coin và gems (như v.0.2)  
- **Starfall Mode**: Chỉ tập trung xem ads để nhận starfall ticket

## 🎯 Các bước thực hiện (Starfall Mode)
1. **Step 1**: Tìm kiếm hình ảnh `ads.png` và click vào đó
2. **Step 2**: Chờ đợi ads chạy xong (30-60 giây)
3. **Step 3**: Tìm nút `Claim.png` và click để nhận starfall ticket
4. **Step 4**: Lặp lại chu trình để tích lũy starfall ticket

## 🔧 Tools và Scripts mới cho v.0.3

### 📁 Cấu trúc file mới
```
auto-click/
├── image/
│   ├── ads.png        # 🆕 Hình ảnh nút xem ads
│   ├── starfall.png   # 🆕 Hình ảnh starfall ticket  
│   └── ...existing files...
├── scripts/           # 🆕 Thư mục scripts v.0.3
│   ├── test_starfall.bat    # Test chế độ starfall
│   ├── switch_mode.bat      # Chuyển đổi chế độ
│   └── auto_setup.bat       # Cài đặt tự động v.0.3
├── config/            # 🆕 Thư mục cấu hình
│   ├── starfall_config.json  # Cấu hình starfall mode
│   └── normal_config.json    # Cấu hình normal mode  
└── ...existing files...
```

### 🚀 Scripts mới

#### 1. **test_starfall.bat** - Test chế độ Starfall
```bash
# Test các hình ảnh starfall mode
scripts/test_starfall.bat
```

#### 2. **switch_mode.bat** - Chuyển đổi chế độ
```bash  
# Chuyển giữa Normal và Starfall mode
scripts/switch_mode.bat
```

#### 3. **auto_setup.bat** - Cài đặt v.0.3
```bash
# Cài đặt tự động tất cả cho v.0.3
scripts/auto_setup.bat
```

#### 4. **build_v3.bat** - Build phiên bản v.0.3
```bash
# Build EXE với tính năng starfall mode
scripts/build_v3.bat
```

### ⚙️ Files cấu hình

#### **starfall_config.json**
```json
{
  "mode": "starfall",
  "ads_wait_time": 45,
  "max_attempts": 20,
  "confidence": 0.7,
  "images": ["ads.png", "Claim.png", "starfall.png"],
  "cycle_delay": 10
}
```

#### **normal_config.json**  
```json
{
  "mode": "normal", 
  "collect_gold": true,
  "collect_gems": true,
  "ads_wait_time": 30,
  "confidence": 0.8,
  "images": ["gold2.png", "gold.png", "coin.png", "Gems.png", "OK.png", "Claim.png"]
}
```

## 🎮 Cách sử dụng v.0.3

### Phương pháp 1: Giao diện GUI (Khuyến nghị)
1. **Chạy ứng dụng**: `python run.py`
2. **Chọn chế độ**: 
   - Nút **"Normal Mode"** (thu lượm + gems)
   - Nút **"Starfall Mode"** (chỉ xem ads)
3. **Cấu hình thời gian**: Điều chỉnh thời gian chờ ads
4. **Bắt đầu**: Click "Start" và theo dõi log

### Phương pháp 2: Scripts tự động
```bash
# Test trước khi chạy
scripts/test_starfall.bat

# Chạy Starfall mode
scripts/switch_mode.bat starfall
python run.py

# Chạy Normal mode  
scripts/switch_mode.bat normal
python run.py
```

### Phương pháp 3: Command line
```bash
# Chạy với tham số chế độ
python run.py --mode starfall
python run.py --mode normal
python run.py --config config/starfall_config.json
```

## 🔍 Tools kiểm tra và debug

### **Debug Mode**
```bash
# Chạy với debug để xem chi tiết
python run.py --debug --mode starfall
```

### **Image Recognition Test**
```bash
# Test nhận diện hình ảnh starfall
python scripts/test_recognition.py --image ads.png
python scripts/test_recognition.py --image starfall.png
```

### **Performance Monitor**
```bash
# Theo dõi hiệu suất
python scripts/monitor_performance.py
```

## 📊 So sánh chế độ

| Tính năng | Normal Mode | Starfall Mode |
|-----------|-------------|---------------|
| **Thu lượm Gold/Coin** | ✅ Có | ❌ Không |
| **Thu lượm Gems** | ✅ Có | ❌ Không |
| **Xem Ads** | ✅ Có | ✅ Có (chính) |
| **Starfall Ticket** | ✅ Có | ✅ Có (tập trung) |
| **Tốc độ** | Chậm hơn | Nhanh hơn |
| **Hiệu quả** | Đa mục tiêu | Chuyên biệt |

## 🎯 Chiến lược sử dụng

### **Chiến lược 1: Cân bằng**
- **Sáng**: Starfall Mode (tích lũy ticket)
- **Chiều**: Normal Mode (thu lượm tổng hợp)

### **Chiến lược 2: Tập trung**  
- **Event Starfall**: Chỉ dùng Starfall Mode
- **Ngày thường**: Chỉ dùng Normal Mode

### **Chiến lược 3: Tự động**
```bash
# Lập lịch tự động
scripts/schedule_auto.bat
# 00:00-12:00: Starfall Mode  
# 12:00-24:00: Normal Mode
```

## Tính năng
- ✅ Giao diện đồ họa với nút Start/Stop
- ✅ Hiển thị số lần click và trạng thái hoạt động
- ✅ Log chi tiết các hoạt động
- ✅ Cấu hình thời gian chờ và độ chính xác
- ✅ Tự động lặp lại chu trình
- ✅ Tính năng dừng khẩn cấp (di chuyển chuột tới góc trái trên)

## Cài đặt

### Bước 1: Cài đặt Python
Đảm bảo máy tính đã cài đặt Python 3.7+ từ [python.org](https://python.org)

### Bước 2: Cài đặt thư viện

**⚠️ Nếu gặp lỗi cài đặt, hãy thử các phương pháp sau:**

#### Phương pháp 1: Cài đặt thông thường
```bash
install.bat
```

#### Phương pháp 2: Cài đặt fix lỗi (khuyến nghị)
```bash
install_fix.bat
```

#### Phương pháp 3: Sử dụng Conda
```bash
install_conda.bat
```

#### Phương pháp 4: Cài đặt thủ công
```bash
pip install -r requirements.txt
```

**📋 Xem chi tiết:** `khac_phuc_loi.md` để biết cách khắc phục các lỗi cụ thể

### Bước 3: Chạy ứng dụng
```bash
python run.py
```

## 🚀 Build thành file EXE

### Cách 1: Sử dụng script tự động (khuyến nghị)

**Trên Windows:**
```bash
# Cách thông thường
build_exe.bat

# Nếu gặp lỗi PyInstaller, dùng script fix
build_exe_fix.bat
```

**Trên Linux/Mac:**
```bash
chmod +x build_exe.sh
./build_exe.sh
```

### 🔧 Khắc phục lỗi PyInstaller

**Nếu gặp lỗi `OSError` hoặc quyền truy cập:**

```bash
# Phương pháp 1: Script khắc phục mạnh
fix_pyinstaller_permission.bat

# Phương pháp 2: Giao diện GUI (dễ dùng)
build_gui.bat

# Phương pháp 3: Sử dụng Nuitka (thay thế PyInstaller)
build_nuitka.bat
```

### Cách 2: Build thủ công
```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Build thành file EXE
pyinstaller --onefile --windowed --name "AutoClicker-GameBot" --add-data "image;image" run.py
```

### 📁 Kết quả sau khi build:
- File EXE sẽ được tạo trong thư mục: `build/dist/`
- Tên file: `AutoClicker-GameBot.exe` (Windows) hoặc `AutoClicker-GameBot` (Linux/Mac)
- Kích thước: ~50-100MB (bao gồm Python runtime)

### 📊 So sánh các phương pháp build:

| Phương pháp | Ưu điểm | Nhược điểm | Kích thước |
|-------------|---------|------------|-----------|
| **PyInstaller** | Phổ biến, ổn định | Chậm, dung lượng lớn | ~80-120MB |
| **Nuitka** | Nhanh, tối ưu | Cần Visual C++ | ~50-80MB |
| **auto-py-to-exe** | GUI thân thiện | Dựa trên PyInstaller | ~80-120MB |
| **cx_Freeze** | Đơn giản, nhẹ | Ít tính năng | ~60-100MB |

### ⚠️ Lưu ý quan trọng:
- **Thư mục image**: Khi chạy file EXE, đảm bảo thư mục `image/` ở cùng vị trí với file EXE
- **Antivirus**: Một số phần mềm diệt virus có thể cảnh báo false positive với file EXE
- **Performance**: File EXE có thể khởi động chậm hơn chạy trực tiếp Python
- **Visual C++**: Nuitka cần Microsoft Visual C++ Redistributable

## Cấu trúc file
```
auto-click/
├── image/              # Thư mục chứa các hình ảnh mẫu
│   ├── Gems.png       # Hình ảnh để click bước 1
│   ├── OK.png         # Nút OK trong popup  
│   ├── Claim.png      # Nút claim phần thưởng
│   ├── coin.png       # Hình ảnh coin
│   ├── gem.png        # Hình ảnh gem
│   ├── gold.png       # Hình ảnh gold
│   └── gold2.png      # Hình ảnh gold loại 2
├── build/             # Thư mục build (tự động tạo)
│   └── dist/          # Chứa file EXE sau khi build
├── auto_clicker.py    # File chính chứa ứng dụng
├── run.py            # Script khởi chạy
├── requirements.txt  # Danh sách thư viện cần thiết
├── .gitignore        # File cấu hình Git ignore
├── COMMIT_TEMPLATE.md # Template cho Git commit messages
├── build_exe.bat     # Script build EXE cho Windows
├── build_exe_fix.bat # Script build EXE (khắc phục lỗi)
├── build_exe.sh      # Script build EXE cho Linux/Mac
├── build_gui.bat     # Build với giao diện GUI (auto-py-to-exe)
├── build_nuitka.bat  # Build với Nuitka (thay thế PyInstaller)
├── fix_pyinstaller_permission.bat # Khắc phục lỗi quyền PyInstaller
├── install.bat       # Script cài đặt cho Windows
├── install_fix.bat   # Script cài đặt fix lỗi
├── install_conda.bat # Script cài đặt với Conda
├── install_pyinstaller.bat # Script cài đặt PyInstaller
└── readme.md         # File hướng dẫn này
```

## Cách sử dụng

1. **Khởi chạy**: Chạy `python run.py` để mở ứng dụng
2. **Cấu hình**: Điều chỉnh thời gian chờ và độ chính xác nếu cần
3. **Bắt đầu**: Click nút "Bắt đầu" để khởi động auto-click
4. **Theo dõi**: Xem log hoạt động và số lần click
5. **Dừng**: Click nút "Dừng lại" hoặc di chuyển chuột tới góc trái trên màn hình

## Lưu ý an toàn
- ⚠️ **Dừng khẩn cấp**: Di chuyển chuột tới góc trái trên màn hình để dừng ngay lập tức
- ⚠️ **Sử dụng có trách nhiệm**: Chỉ sử dụng cho mục đích hợp pháp
- ⚠️ **Backup dữ liệu**: Sao lưu dữ liệu quan trọng trước khi sử dụng

## Troubleshooting

### Không tìm thấy hình ảnh
- Đảm bảo các file hình ảnh có trong thư mục `image/`
- Kiểm tra độ phân giải màn hình
- Điều chỉnh độ chính xác (confidence) thấp hơn

### Ứng dụng không click đúng vị trí
- Kiểm tra tỷ lệ scale màn hình
- Đảm bảo game hiển thị đầy đủ trên màn hình
- Tăng thời gian chờ giữa các bước

### Hiệu suất chậm
- Giảm độ chính xác nhận diện hình ảnh
- Tăng thời gian pause giữa các lệnh
- Đóng các ứng dụng không cần thiết

### Lỗi build EXE

**Lỗi `OSError` khi cài PyInstaller:**
```bash
# Chạy Command Prompt với quyền Administrator
# Sau đó: install_pyinstaller.bat
```

**Lỗi `pyinstaller not found`:**
```bash
# Thử các lệnh sau:
python -m pip install pyinstaller
pip install --user pyinstaller
pip install --no-cache-dir pyinstaller
```

**File EXE không chạy được:**
- Đảm bảo thư mục `image/` ở cùng vị trí với file EXE
- Tắt antivirus tạm thời
- Chạy file EXE với quyền Administrator

**Build thất bại:**
- Kiểm tra Python version >= 3.7
- Đảm bảo tất cả dependencies đã cài đặt
- Thử build với `build_exe_fix.bat`

## Thông tin kỹ thuật
- **Python version**: 3.7+
- **GUI Framework**: Tkinter
- **Image Recognition**: OpenCV
- **Auto-clicking**: PyAutoGUI
- **Image Processing**: Pillow


## 📦 Git và Version Control

### 🎯 Khởi tạo Git repository:
```bash
git init
git add .
git commit -m "Initial commit: Auto Clicker v0.2"
```

### 📋 File được ignore tự động:
- ✅ Thư mục `build/` và `dist/` (file build)
- ✅ `__pycache__/` và `*.pyc` (Python cache)
- ✅ `venv/` và `.venv/` (virtual environments)
- ✅ `.vscode/` và `.idea/` (IDE settings)
- ✅ `*.log` và `*.tmp` (file tạm thời)
- ✅ OS files (`.DS_Store`, `Thumbs.db`)

### 🔄 Clone project:
```bash
git clone <repository-url>
cd auto-click
pip install -r requirements.txt
python run.py
```

### 📝 Commit message template:
Project bao gồm file `COMMIT_TEMPLATE.md` với các mẫu commit message:
- ✨ `feat:` - Tính năng mới
- 🐛 `fix:` - Sửa lỗi  
- 📚 `docs:` - Cập nhật tài liệu
- 🔧 `chore:` - Bảo trì code
- ⚡ `perf:` - Tối ưu hiệu suất

## Update v.0.2.
- Ở step 1, bot sẽ **thu lượm tất cả** các loại vàng/coin trước khi tìm Gems.png:
  - `gold2.png` - Vàng loại 2 (ưu tiên cao nhất)
  - `gold.png` - Vàng thường
  - `coin.png` - Đồng xu
- Tính năng **thu lượm nhiều lần liên tiếp**: Bot sẽ tìm kiếm và click tất cả gold/coin có thể tìm thấy (tối đa 10 lần) trong một chu kỳ
- Sau khi thu lượm hết gold/coin, mới chuyển sang tìm `Gems.png`