# Auto Clicker - Game Bot

## Mô tả
Ứng dụng auto-click được viết bằng Python để tự động hóa việc click trong game. Ứng dụng sẽ tự động tìm kiếm và click vào các hình ảnh cụ thể theo trình tự được định sẵn.

## Các bước thực hiện
1. **Step 1**: Tìm kiếm hình ảnh `Gems.png` và click vào đó
2. **Step 2**: Đợi popup hiện lên và tìm kiếm nút `OK.png` rồi click  
3. **Step 3**: Chờ đợi ads chạy xong, tìm nút `Claim.png` rồi click để nhận thưởng

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

## Cấu trúc file
```
auto-click/
├── image/              # Thư mục chứa các hình ảnh mẫu
│   ├── Gems.png       # Hình ảnh để click bước 1
│   ├── OK.png         # Nút OK trong popup  
│   ├── Claim.png      # Nút claim phần thưởng
│   ├── coin.png       # Hình ảnh coin
│   ├── gem.png        # Hình ảnh gem
│   └── gold.png       # Hình ảnh gold
├── auto_clicker.py    # File chính chứa ứng dụng
├── run.py            # Script khởi chạy
├── requirements.txt  # Danh sách thư viện cần thiết
├── install.bat       # Script cài đặt cho Windows
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

## Thông tin kỹ thuật
- **Python version**: 3.7+
- **GUI Framework**: Tkinter
- **Image Recognition**: OpenCV
- **Auto-clicking**: PyAutoGUI
- **Image Processing**: Pillow


## Update v.0.2.
- Ở step 1, bot sẽ **thu lượm tất cả** các loại vàng/coin trước khi tìm Gems.png:
  - `gold2.png` - Vàng loại 2 (ưu tiên cao nhất)
  - `gold.png` - Vàng thường
  - `coin.png` - Đồng xu
- Tính năng **thu lượm nhiều lần liên tiếp**: Bot sẽ tìm kiếm và click tất cả gold/coin có thể tìm thấy (tối đa 10 lần) trong một chu kỳ
- Sau khi thu lượm hết gold/coin, mới chuyển sang tìm `Gems.png`