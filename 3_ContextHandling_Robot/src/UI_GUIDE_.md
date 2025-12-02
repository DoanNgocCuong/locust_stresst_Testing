# 🎨 Hướng Dẫn Sử Dụng Locust Web UI

## 📖 Tổng Quan

Locust có sẵn **Web UI** rất mạnh mẽ để:
- ⚡ Chạy stress test với giao diện trực quan
- 📊 Xem kết quả real-time
- 📈 Phân tích performance metrics
- 🎯 Điều chỉnh test parameters dễ dàng

## 🚀 Cách Chạy Web UI

### Phương Pháp 1: Sử dụng Script (Recommended)

```powershell
# Chạy với UI mặc định
.\run_ui.ps1

# Hoặc chỉ định port khác
.\run_ui.ps1 -Port 9090
```

### Phương Pháp 2: Chạy trực tiếp

```powershell
locust -f locustfile.py --host=http://103.253.20.30:30020
```

Sau đó mở browser tại: **http://localhost:8089**

## 🖥️ Giao Diện Web UI

### 1. Trang Chủ (Start Page)

Khi mở `http://localhost:8089`, bạn sẽ thấy:

```
┌─────────────────────────────────────┐
│  Locust                            │
├─────────────────────────────────────┤
│  Number of users: [____]           │
│  Spawn rate:      [____]            │
│  Host:            [http://...]      │
│                                    │
│  [Start swarming]                  │
└─────────────────────────────────────┘
```

**Các thông số:**
- **Number of users**: Số lượng concurrent users (VD: 10, 50, 100)
- **Spawn rate**: Số users được tạo mỗi giây (VD: 2, 5, 10)
- **Host**: Base URL của API (đã được set sẵn)

### 2. Dashboard (Khi Test Đang Chạy)

Sau khi click "Start swarming", bạn sẽ thấy dashboard với:

#### 📊 Statistics Table

| Type | Name | # requests | # fails | Median | 95%ile | 99%ile | Average | Min | Max | Content Size | # reqs/sec |
|------|------|-------------|---------|--------|--------|--------|---------|-----|-----|--------------|------------|
| POST | /v1/conversations/end | 150 | 0 | 245 | 450 | 680 | 250 | 120 | 680 | 120 | 2.5 |
| POST | /v1/activities/suggest | 150 | 0 | 180 | 320 | 450 | 185 | 100 | 450 | 80 | 2.5 |
| Aggregated | | 300 | 0 | 210 | 380 | 550 | 217 | 100 | 680 | 100 | 5.0 |

**Giải thích các metrics:**
- **# requests**: Tổng số requests đã gửi
- **# fails**: Số requests bị lỗi
- **Median**: Thời gian response trung bình (50th percentile)
- **95%ile**: 95% requests có response time ≤ giá trị này
- **99%ile**: 99% requests có response time ≤ giá trị này
- **Average**: Thời gian response trung bình
- **Min/Max**: Thời gian response nhỏ nhất/lớn nhất
- **# reqs/sec**: Số requests mỗi giây (RPS)

#### 📈 Charts

1. **Total Requests per Second (RPS)**
   - Biểu đồ hiển thị số requests mỗi giây theo thời gian
   - Giúp xem throughput của hệ thống

2. **Response Times (ms)**
   - Biểu đồ hiển thị response time theo thời gian
   - Có thể xem min, max, median, p95, p99

3. **Number of Users**
   - Biểu đồ hiển thị số lượng users đang chạy

#### ⚠️ Failures Tab

Hiển thị danh sách các requests bị lỗi:
- Method và URL
- Error message
- Occurrences (số lần lỗi)
- Response time

#### 📥 Download Data

Có thể download:
- **CSV**: Statistics dạng CSV
- **Stats History**: Lịch sử statistics

## 🎯 Best Practices

### 1. Bắt Đầu Nhỏ

```
Users: 5
Spawn Rate: 1
```

Sau đó tăng dần:
```
Users: 10 → 20 → 50 → 100
Spawn Rate: 2 → 5 → 10
```

### 2. Quan Sát Metrics

- **Response Time**: Nếu tăng đột ngột → hệ thống đang quá tải
- **Failures**: Nếu có nhiều failures → kiểm tra API server
- **RPS**: Xem throughput tối đa hệ thống có thể xử lý

### 3. Test Scenarios

#### Scenario 1: Light Load
```
Users: 10
Spawn Rate: 2
Duration: 2 minutes
```

#### Scenario 2: Medium Load
```
Users: 50
Spawn Rate: 5
Duration: 5 minutes
```

#### Scenario 3: Heavy Load
```
Users: 100
Spawn Rate: 10
Duration: 10 minutes
```

## 🔧 Advanced Options

### Chạy với Custom Port

```powershell
locust -f locustfile.py --host=http://103.253.20.30:30020 --web-port=9090
```

### Chạy với Custom Host

```powershell
locust -f locustfile.py --host=http://103.253.20.30:30020 --web-host=0.0.0.0
```

### Chạy Headless và Export Report

```powershell
.\run_ui_headless.ps1 -Users 50 -SpawnRate 5 -Time 5m
```

Report sẽ được lưu trong thư mục `results/`

## 📊 Đọc Kết Quả

### Response Time Thresholds

- **< 200ms**: Excellent ✅
- **200-500ms**: Good ✅
- **500-1000ms**: Acceptable ⚠️
- **> 1000ms**: Poor ❌

### Failure Rate

- **0%**: Perfect ✅
- **< 1%**: Good ✅
- **1-5%**: Acceptable ⚠️
- **> 5%**: Poor ❌

### RPS (Requests Per Second)

- Xem RPS tối đa hệ thống có thể xử lý
- Nếu RPS không tăng khi tăng users → bottleneck

## 🐛 Troubleshooting

### UI không mở được

1. Kiểm tra port 8089 có bị chiếm không:
```powershell
netstat -ano | findstr :8089
```

2. Thử port khác:
```powershell
.\run_ui.ps1 -Port 9090
```

### Test không chạy

1. Kiểm tra API server có đang chạy không
2. Kiểm tra network connection
3. Xem logs trong terminal

### Kết quả không chính xác

1. Đảm bảo không có cache
2. Chạy test nhiều lần và lấy trung bình
3. Kiểm tra server resources (CPU, Memory)

## 📚 Tài Liệu Tham Khảo

- [Locust Official Docs](https://docs.locust.io/)
- [Locust Web UI Guide](https://docs.locust.io/en/stable/web-ui.html)

