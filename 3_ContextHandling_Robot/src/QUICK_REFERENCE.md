# ⚡ Quick Reference - Locust Metrics

## 🎯 Câu Hỏi Thường Gặp

### **Q: 10 users, RPS 5 là sao?**

**A:** 
- **10 users** = 10 người dùng ảo chạy đồng thời
- **RPS 5** = Gửi 5 requests mỗi giây
- **Giải thích**: Với `wait_time = between(1, 3)` giây, mỗi user gửi ~0.5 req/s
  - **10 users × 0.5 req/s = 5 RPS** ✅

### **Q: Làm sao để tăng RPS?**

**A:** 3 cách:
1. **Tăng số users**: `-u 20` → RPS tăng gấp đôi
2. **Giảm wait time**: `wait_time = between(0.5, 1.5)` → RPS tăng
3. **Cả hai**: Tăng users + giảm wait time

### **Q: RPS bao nhiêu là tốt?**

**A:** Phụ thuộc vào:
- **Server capacity**: Server có thể xử lý bao nhiêu?
- **Response time**: RPS cao nhưng response time cao → không tốt
- **Failure rate**: RPS cao nhưng nhiều lỗi → không tốt

**Thông thường:**
- **RPS 5-10**: Test nhẹ
- **RPS 20-50**: Test trung bình
- **RPS 50-100+**: Stress test

### **Q: Tại sao RPS không tăng khi tăng users?**

**A:** Có thể do:
- **Server bottleneck**: Server đã đạt giới hạn
- **Network limit**: Băng thông bị giới hạn
- **Wait time quá dài**: Users đợi lâu giữa các requests

## 📊 Công Thức Nhanh

```
RPS ≈ Users / Average Wait Time

Ví dụ:
- 10 users, wait 2 giây → RPS ≈ 5
- 20 users, wait 2 giây → RPS ≈ 10
- 10 users, wait 1 giây → RPS ≈ 10
```

## 🎛️ Các Thông Số Quan Trọng

| Metric | Ý Nghĩa | Giá Trị Tốt |
|--------|---------|-------------|
| **Users** | Số users đồng thời | 10-100 |
| **RPS** | Requests/giây | 5-50 |
| **Avg** | Response time TB | < 500ms |
| **95%ile** | 95% requests ≤ | < 1000ms |
| **Failures** | Tỷ lệ lỗi | < 1% |

## 🚀 Commands Nhanh

```powershell
# Test nhẹ (10 users, RPS ~5)
locust -f locustfile.py --host=... -u 10 -r 2

# Test trung bình (50 users, RPS ~25)
locust -f locustfile.py --host=... -u 50 -r 5

# Test nặng (100 users, RPS ~50)
locust -f locustfile.py --host=... -u 100 -r 10
```


