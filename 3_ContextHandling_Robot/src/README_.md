# Locust Stress Test - Context Handling Robot

Test suite cho stress testing các API của Context Handling Robot.

## 📁 Cấu Trúc Project

```
src/
├── locustfile.py          # File chính chứa Locust tasks
├── config.py              # Configuration và constants
├── data_generators.py     # Classes generate test data
├── requirements.txt        # Python dependencies
├── run_ui.ps1            # Script chạy với Web UI
├── run_ui_headless.ps1    # Script chạy headless mode
├── dashboard.html         # Custom dashboard HTML
├── UI_GUIDE.md           # Hướng dẫn sử dụng Web UI
└── README.md             # Documentation này
```

## 🚀 Cài Đặt

1. Cài đặt dependencies:
```powershell
pip install -r requirements.txt
```

## 🎨 Chạy Test với Web UI (Recommended)

### Cách 1: Sử dụng Script

```powershell
.\run_ui.ps1
```

Sau đó mở browser tại: **http://localhost:8089**

### Cách 2: Chạy trực tiếp

```powershell
locust -f locustfile.py --host=http://103.253.20.30:30020
```

### Mở Custom Dashboard

Mở file `dashboard.html` trong browser để xem thông tin tổng quan.

## 🤖 Chạy Headless (Không có UI)

```powershell
.\run_ui_headless.ps1 -Users 10 -SpawnRate 2 -Time 60s
```

Hoặc:

```powershell
locust -f locustfile.py --host=http://103.253.20.30:30020 --headless -u 10 -r 2 -t 60s
```

**Parameters:**
- `-u 10`: 10 concurrent users
- `-r 2`: Spawn rate 2 users/second
- `-t 60s`: Chạy trong 60 giây

## 📊 API Endpoints được Test

### 1. POST /v1/conversations/end
- **Mục đích**: Kết thúc một conversation
- **Payload**: Chứa conversation_id, user_id, bot info, và conversation_logs
- **Weight**: 1 (có thể điều chỉnh trong `config.py`)

### 2. POST /v1/activities/suggest
- **Mục đích**: Lấy gợi ý activities cho user
- **Payload**: Chỉ chứa user_id
- **Weight**: 1 (có thể điều chỉnh trong `config.py`)

## ⚙️ Cấu Hình

Các cấu hình có thể thay đổi trong file `config.py`:
- `BASE_URL`: Base URL của API server
- `WEIGHT_CONVERSATION_END`: Tỷ lệ thực thi task conversation end
- `WEIGHT_ACTIVITIES_SUGGEST`: Tỷ lệ thực thi task activities suggest

## 🏗️ Nguyên Tắc SOLID

Code được thiết kế theo nguyên tắc SOLID:

1. **Single Responsibility**: Mỗi class có một trách nhiệm duy nhất
   - `ConversationLogGenerator`: Chỉ generate conversation logs
   - `ConversationDataGenerator`: Chỉ generate data cho conversation API
   - `ActivitySuggestDataGenerator`: Chỉ generate data cho activity API
   - `ContextHandlingRobotUser`: Chỉ định nghĩa và thực thi tasks

2. **Open/Closed**: Dễ dàng mở rộng thêm generators hoặc tasks mới mà không cần sửa code cũ

3. **Dependency Inversion**: Sử dụng dependency injection thông qua imports

## 📈 Kết Quả Test

Sau khi chạy test, Locust sẽ hiển thị:
- Total Requests
- Requests per second (RPS)
- Response times (min, max, median, p95, p99)
- Number of failures
- Response time distribution

## 📖 Tài Liệu

- Xem `UI_GUIDE.md` để biết cách sử dụng Web UI chi tiết
- Xem `dashboard.html` để xem custom dashboard

## 🐛 Troubleshooting

### Lỗi import module
Đảm bảo bạn đang chạy từ thư mục `src/`:
```powershell
cd src
.\run_ui.ps1
```

### Lỗi connection refused
Kiểm tra:
- API server có đang chạy không
- Base URL trong `config.py` có đúng không
- Firewall/network có block connection không

### Lỗi port đã được sử dụng
Thử port khác:
```powershell
.\run_ui.ps1 -Port 9090
```
