# 🔐 Hướng Dẫn Sử Dụng .env File

## 📋 Tổng Quan

Project sử dụng file `.env` để lưu trữ các cấu hình nhạy cảm và có thể thay đổi như URL của API server.

## 🚀 Cài Đặt

### Bước 1: Tạo file .env

Copy file `.env.example` thành `.env`:

```powershell
cd 3_ContextHandling_Robot
copy .env.example .env
```

### Bước 2: Cập nhật giá trị

Mở file `.env` và cập nhật URL:

```env
# Context Handling Robot API Configuration
3_ContextHandling_Robot_URL=http://103.253.20.30:30020
```

### Bước 3: Cài đặt dependencies

```powershell
cd src
pip install -r requirements.txt
```

## 📝 Cấu Trúc File .env

```env
# Context Handling Robot API Configuration
3_ContextHandling_Robot_URL=http://103.253.20.30:30020
```

## 🔧 Cách Hoạt Động

### Python Code (config.py)

File `config.py` tự động đọc từ `.env`:

```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

BASE_URL = os.getenv('3_ContextHandling_Robot_URL', 'http://103.253.20.30:30020')
```

### PowerShell Scripts

Scripts PowerShell (`run_ui.ps1`, `run_ui_headless.ps1`) cũng tự động đọc từ `.env`:

```powershell
# Script tự động tìm và đọc .env file
$envFile = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
```

## 🎯 Sử Dụng

### Chạy với .env (Recommended)

```powershell
# Script tự động đọc từ .env
.\run_ui.ps1
```

### Override với parameter

```powershell
# Override URL từ .env
.\run_ui.ps1 -Host "http://other-server:30020"
```

## 🔒 Bảo Mật

- File `.env` đã được thêm vào `.gitignore`
- **KHÔNG** commit file `.env` lên Git
- Chỉ commit file `.env.example` làm template

## 📋 Checklist

- [ ] Copy `.env.example` thành `.env`
- [ ] Cập nhật URL trong `.env`
- [ ] Cài đặt `python-dotenv`: `pip install -r requirements.txt`
- [ ] Test chạy script để đảm bảo đọc được `.env`

## 🐛 Troubleshooting

### Lỗi: "ModuleNotFoundError: No module named 'dotenv'"

**Giải pháp:**
```powershell
pip install python-dotenv
```

### Lỗi: Script không đọc được .env

**Kiểm tra:**
1. File `.env` có tồn tại trong thư mục `3_ContextHandling_Robot/` không?
2. Tên biến có đúng `3_ContextHandling_Robot_URL` không?
3. Format có đúng `KEY=VALUE` không?

### Lỗi: "Warning: .env file not found"

**Giải pháp:**
- Script sẽ sử dụng default URL
- Hoặc tạo file `.env` từ `.env.example`

## 📚 Tài Liệu Tham Khảo

- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)








