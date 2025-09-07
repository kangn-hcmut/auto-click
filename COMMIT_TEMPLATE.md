# Git Commit Message Template

## 📝 Các loại commit thường dùng:

### ✨ Features (Tính năng mới)
```
feat: add gold collection feature
feat: implement multi-coin detection
feat: create GUI build interface
```

### 🐛 Bug Fixes (Sửa lỗi)
```
fix: resolve PyInstaller permission error
fix: image detection accuracy issue
fix: application crash on startup
```

### 📚 Documentation (Tài liệu)
```
docs: update README with build instructions
docs: add troubleshooting section
docs: create installation guide
```

### 🔧 Maintenance (Bảo trì)
```
chore: add .gitignore file
chore: update dependencies
chore: clean up build files
```

### 🎨 Style/Refactor (Tái cấu trúc)
```
style: improve code formatting
refactor: optimize image search algorithm
refactor: separate GUI and logic components
```

### ⚡ Performance (Hiệu suất)
```
perf: optimize image detection speed
perf: reduce memory usage in main loop
```

### 🚀 Build/Deploy (Build/Deploy)
```
build: add PyInstaller configuration
build: create Nuitka build script
deploy: setup automatic EXE generation
```

## 🏷️ Version Tags:
```
git tag -a v0.2.0 -m "Version 0.2: Multi-gold collection feature"
git tag -a v0.2.1 -m "Version 0.2.1: Fix build issues"
```

## 📦 Useful Git Commands:

### Khởi tạo repository:
```bash
git init
git add .
git commit -m "feat: initial Auto Clicker v0.2 with multi-gold collection"
```

### Push lên GitHub:
```bash
git remote add origin https://github.com/username/auto-click.git
git branch -M main
git push -u origin main
```

### Tạo release:
```bash
git tag -a v0.2.0 -m "Auto Clicker v0.2 - Multi-gold collection"
git push origin v0.2.0
```
