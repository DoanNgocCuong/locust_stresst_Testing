# 📊 CCU vs RPS - Giải Thích và Cách Điều Chỉnh

## ✅ Hiểu Đúng: 25 CCU → ~11 RPS là Bình Thường

### Công Thức Tính RPS

```
RPS ≈ CCU / (Response Time + Wait Time)
```

### Ví Dụ Thực Tế

**Cấu hình hiện tại:**
- CCU = 25 users
- Response Time (trung bình) = ~120ms = 0.12 giây
- Wait Time = `between(1.0, 3.0)` = trung bình 2.0 giây

**Tính toán:**
```
Mỗi vòng = Response Time + Wait Time
         = 0.12 + 2.0
         = 2.12 giây

RPS = 25 / 2.12 ≈ 11.8 RPS
```

**Kết quả:** ~11-12 RPS ✅ **Đúng như mong đợi!**

## 🔍 Tại Sao Không Phải 25 RPS?

**Sai lầm phổ biến:** Nghĩ rằng 25 CCU = 25 RPS

**Thực tế:**
- CCU = Số users **đồng thời** đang chạy
- RPS = Số requests **mỗi giây** được gửi đi
- RPS phụ thuộc vào:
  1. **Response Time** (thời gian server xử lý)
  2. **Wait Time** (thời gian chờ giữa các requests)

## 📈 Bảng So Sánh

| CCU | Response Time | Wait Time | RPS Tính Toán | Giải Thích |
|-----|---------------|-----------|---------------|------------|
| 25  | 120ms         | 1-3s (avg 2s) | ~11 RPS | Hiện tại |
| 25  | 120ms         | 0.1-0.5s (avg 0.3s) | ~60 RPS | Nếu giảm wait_time |
| 25  | 500ms         | 1-3s (avg 2s) | ~10 RPS | Nếu server chậm hơn |
| 25  | 50ms          | 0.1-0.5s (avg 0.3s) | ~71 RPS | Server nhanh + wait_time thấp |

## ⚙️ Cấu Hình Hiện Tại

### File: `config.py`

```python
WAIT_TIME_MIN = 1.0  # giây
WAIT_TIME_MAX = 3.0  # giây
```

### File: `locustfile.py`

```python
wait_time = between(Config.WAIT_TIME_MIN, Config.WAIT_TIME_MAX)
```

## 🎯 Cách Điều Chỉnh RPS

### 1. Giảm Wait Time (Tăng RPS)

**Mục đích:** Stress test nặng hơn, ép server xử lý nhiều requests hơn

**Cách 1: Sửa trong code**

```python
# config.py
WAIT_TIME_MIN = 0.1  # Giảm từ 1.0 xuống 0.1
WAIT_TIME_MAX = 0.5  # Giảm từ 3.0 xuống 0.5
```

**Cách 2: Dùng environment variable**

```bash
# .env hoặc export
QWEN_API_WAIT_MIN=0.1
QWEN_API_WAIT_MAX=0.5
```

**Kết quả:**
```
RPS ≈ 25 / (0.12 + 0.3) ≈ 60 RPS
```

### 2. Tăng Wait Time (Giảm RPS)

**Mục đích:** Load test nhẹ hơn, mô phỏng user thật hơn (user thường không gửi request liên tục)

```python
WAIT_TIME_MIN = 2.0
WAIT_TIME_MAX = 5.0
```

**Kết quả:**
```
RPS ≈ 25 / (0.12 + 3.5) ≈ 7 RPS
```

### 3. Giữ Wait Time, Tăng CCU (Tăng RPS)

**Mục đích:** Tăng số users đồng thời để tăng RPS

```
CCU = 50 users
RPS ≈ 50 / 2.12 ≈ 24 RPS
```

## 📝 Khi Nào Dùng Wait Time Nào?

### Wait Time Thấp (0.1-0.5s)
- ✅ **Stress Test**: Ép server xử lý tối đa
- ✅ **Performance Test**: Tìm giới hạn của hệ thống
- ⚠️ **Không giống user thật**: User thật không gửi request liên tục

### Wait Time Trung Bình (1-3s) - **Hiện tại**
- ✅ **Load Test**: Mô phỏng user thật
- ✅ **Stability Test**: Test hệ thống ổn định
- ✅ **Phù hợp cho hầu hết các trường hợp**

### Wait Time Cao (3-10s)
- ✅ **Realistic Load Test**: Mô phỏng chính xác hành vi user
- ✅ **Long Running Test**: Test hệ thống trong thời gian dài
- ⚠️ **RPS thấp**: Cần nhiều users để đạt RPS mong muốn

## 🔧 Ví Dụ Điều Chỉnh

### Scenario 1: Muốn 25 CCU → ~25 RPS

```python
# config.py
WAIT_TIME_MIN = 0.1
WAIT_TIME_MAX = 0.3

# Tính toán:
# RPS ≈ 25 / (0.12 + 0.2) ≈ 78 RPS (cao hơn mong muốn)
# Nếu muốn ~25 RPS, cần giảm CCU hoặc tăng wait_time
```

### Scenario 2: Muốn Test Nặng (Stress Test)

```python
# config.py
WAIT_TIME_MIN = 0.0  # Không chờ
WAIT_TIME_MAX = 0.1  # Chờ rất ít

# Tính toán:
# RPS ≈ 25 / (0.12 + 0.05) ≈ 147 RPS
# ⚠️ Cảnh báo: Server có thể bị quá tải!
```

### Scenario 3: Muốn Test Nhẹ (Load Test)

```python
# config.py - Giữ nguyên
WAIT_TIME_MIN = 1.0
WAIT_TIME_MAX = 3.0

# RPS ≈ 11-12 RPS (như hiện tại)
```

## ✅ Kết Luận

1. **25 CCU → ~11 RPS là BÌNH THƯỜNG** với wait_time = 1-3s
2. **RPS phụ thuộc vào:** Response Time + Wait Time
3. **Muốn tăng RPS:** Giảm wait_time hoặc tăng CCU
4. **Muốn test thực tế:** Giữ wait_time 1-3s (như hiện tại)
5. **Muốn stress test:** Giảm wait_time xuống 0.1-0.5s

## 📊 Monitoring

Khi chạy test, theo dõi:
- **Response Time**: Nếu tăng cao → server đang quá tải
- **RPS**: So sánh với công thức tính toán
- **Error Rate**: Nếu tăng → giảm RPS hoặc tăng wait_time












