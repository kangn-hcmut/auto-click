# Khắc phục lỗi cài đặt

## Lỗi thường gặp và cách khắc phục

### 1. Lỗi build numpy trên Windows

**Triệu chứng:**
```
Getting requirements to build wheel did not run successfully.
error: subprocess-exited-with-error
```

**Cách khắc phục:**

#### Phương pháp 1: Sử dụng pre-compiled wheel
```bash
python -m pip install --upgrade pip
python -m pip install numpy --only-binary=all
python -m pip install pyautogui Pillow opencv-python
```

#### Phương pháp 2: Chạy script cài đặt fix
```bash
install_fix.bat
```

#### Phương pháp 3: Sử dụng Conda
```bash
# Cài đặt Miniconda từ: https://docs.conda.io/en/latest/miniconda.html
# Sau đó chạy:
install_conda.bat
```

### 2. Thiếu Visual Studio Build Tools

**Nếu vẫn gặp lỗi build:**

1. **Cài đặt Microsoft C++ Build Tools:**
   - Download từ: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Chọn "C++ build tools" và cài đặt

2. **Hoặc cài đặt Visual Studio Community:**
   - Download từ: https://visualstudio.microsoft.com/downloads/
   - Chọn "Desktop development with C++" workload

### 3. Lỗi permission

**Nếu gặp lỗi quyền truy cập:**
```bash
# Cài đặt cho user hiện tại
python -m pip install --user opencv-python pyautogui Pillow numpy
```

### 4. Lỗi proxy/network

**Nếu ở môi trường có proxy:**
```bash
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org opencv-python pyautogui Pillow numpy
```

### 5. Phiên bản Python không tương thích

**Kiểm tra phiên bản Python:**
```bash
python --version
```

**Yêu cầu:** Python 3.7 đến 3.11 (tránh Python 3.12 mới nhất có thể có vấn đề tương thích)

### 6. Cài đặt từng thư viện riêng lẻ

**Nếu cài đặt hàng loạt bị lỗi:**
```bash
# Cài từng cái một
python -m pip install numpy
python -m pip install Pillow
python -m pip install pyautogui
python -m pip install opencv-python
```

### 7. Sử dụng virtual environment

**Tạo môi trường ảo sạch:**
```bash
python -m venv auto_clicker_env
auto_clicker_env\Scripts\activate
python -m pip install --upgrade pip
python -m pip install opencv-python pyautogui Pillow numpy
```

## Test cài đặt

**Sau khi cài đặt, test bằng:**
```bash
python demo_test.py
```

**Hoặc test nhanh:**
```bash
python -c "import cv2, pyautogui, numpy, PIL; print('OK!')"
```

## Liên hệ hỗ trợ

Nếu vẫn gặp vấn đề, vui lòng:
1. Chụp screenshot lỗi đầy đủ
2. Cho biết phiên bản Python (`python --version`)
3. Cho biết hệ điều hành Windows version
4. Đã thử phương pháp nào ở trên

---
*Cập nhật: Các lỗi cài đặt thường do thiếu build tools hoặc phiên bản Python quá mới.*
