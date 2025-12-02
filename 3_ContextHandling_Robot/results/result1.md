# 📊 Báo Cáo Kết Quả Stress Test - Context Handling Robot API

**Ngày test:** 2025-12-02  
**Test Tool:** Locust 2.42.6  
**Target Server:** http://103.253.20.30:30020

---

## 🎯 Tổng Quan Test

### Test Configuration
- **Số Users:** 200 concurrent users
- **Status:** RUNNING
- **Wait Time:** 1-3 giây giữa các requests

### API Endpoints Tested
1. **POST /v1/conversations/end** - Kết thúc conversation
2. **POST /v1/activities/suggest** - Gợi ý activities cho user

---

## 📈 Kết Quả Test

### Screenshot: Real-time Dashboard
![Test Results Dashboard](image/result/1764649092830.png)

---

## 📊 Phân Tích Chi Tiết

### 1. Performance Metrics

#### **POST /v1/activities/suggest**
- **Total Requests:** 5,577
- **Failures:** 0 (0.00%)
- **Average Response Time:** 749.37 ms
- **Min Response Time:** 27 ms
- **Max Response Time:** 2,268 ms
- **Median (50th percentile):** 690 ms
- **95th percentile:** 1,700 ms
- **99th percentile:** 1,900 ms
- **Average Size:** 23,780.29 bytes
- **Current RPS:** 29.4 req/s
- **Current Failures/s:** 0

#### **POST /v1/conversations/end**
- **Total Requests:** 5,699
- **Failures:** 0 (0.00%)
- **Average Response Time:** 714.25 ms
- **Min Response Time:** 15 ms
- **Max Response Time:** 2,271 ms
- **Median (50th percentile):** 590 ms
- **95th percentile:** 1,700 ms
- **99th percentile:** 1,900 ms
- **Average Size:** 3,997.9 bytes
- **Current RPS:** 28.2 req/s
- **Current Failures/s:** 0

#### **Aggregated (Tổng Hợp)**
- **Total Requests:** 11,276
- **Total Failures:** 0 (0.00%)
- **Average Response Time:** 731.62 ms
- **Min Response Time:** 15 ms
- **Max Response Time:** 2,271 ms
- **Median (50th percentile):** 640 ms
- **95th percentile:** 1,700 ms
- **99th percentile:** 1,900 ms
- **Average Size:** 13,782.08 bytes
- **Total RPS:** 57.6 req/s
- **Current Failures/s:** 0

---

## ✅ Đánh Giá Kết Quả

### Performance Assessment

#### Response Time Analysis
- **Average Response Time:** 731.62 ms - ⚠️ **Acceptable** (500-1000ms range)
- **Median Response Time:** 640 ms - ⚠️ **Acceptable**
- **95th Percentile:** 1,700 ms - ⚠️ **Acceptable** (cần cải thiện)
- **99th Percentile:** 1,900 ms - ⚠️ **Acceptable**

**Phân bổ Response Time:**
- ✅ **Excellent** (< 200ms): Một số requests nhanh (Min: 15-27ms)
- ✅ **Good** (200-500ms): Một phần requests
- ⚠️ **Acceptable** (500-1000ms): Phần lớn requests (Median: 640ms, Average: 731ms)
- ⚠️ **High** (> 1000ms): Một số requests ở 95th và 99th percentile (1,700-1,900ms)

#### Failure Analysis
- **Total Failures:** 0
- **Failure Rate:** 0.00%
- **Status:** ✅ **Perfect - No failures!**
- **Main Failure Reasons:** Không có failures

#### Throughput Analysis
- **Current RPS:** 57.6 req/s
- **Peak RPS:** 57.6 req/s (tại thời điểm test)
- **RPS per Endpoint:**
  - `/v1/activities/suggest`: 29.4 req/s
  - `/v1/conversations/end`: 28.2 req/s
- **RPS Stability:** ✅ **Stable** - RPS ổn định với 200 users

#### Load Analysis
- **Total Requests:** 11,276 requests
- **Concurrent Users:** 200 users
- **Request Distribution:**
  - Activities suggest: 49.5% (5,577 requests)
  - Conversations end: 50.5% (5,699 requests)
- **Balance:** ✅ **Well balanced** - Tỷ lệ requests gần như 50/50

---

## 🎯 Kết Luận

### ✅ Điểm Mạnh

1. **Zero Failures** - Không có failures nào trong suốt quá trình test với 200 concurrent users
2. **High Throughput** - Đạt 57.6 RPS với 200 users, cho thấy server có khả năng xử lý tốt
3. **Stable Performance** - RPS ổn định, không có biến động lớn
4. **Good Load Distribution** - Requests được phân bổ đều giữa 2 endpoints
5. **Fast Min Response Time** - Một số requests rất nhanh (15-27ms) cho thấy server có khả năng xử lý nhanh khi không bị quá tải

### ⚠️ Điểm Cần Cải Thiện

1. **Response Time ở 95th Percentile** - 1,700ms là hơi cao, cần tối ưu để đảm bảo 95% requests < 1000ms
2. **Average Response Time** - 731ms là acceptable nhưng có thể cải thiện xuống < 500ms
3. **99th Percentile** - 1,900ms cho thấy một số requests bị delay, cần investigate nguyên nhân

### 📋 Khuyến Nghị

1. **Ngắn hạn:**
   - ✅ **Maintain current performance** - Server đang hoạt động tốt với 0% failures
   - 🔍 **Investigate slow requests** - Tìm hiểu tại sao một số requests ở 95th/99th percentile lại chậm (1,700-1,900ms)
   - 📊 **Monitor response time distribution** - Xem có pattern nào trong các requests chậm không

2. **Dài hạn:**
   - ⚡ **Optimize response time** - Tối ưu để đạt 95th percentile < 1000ms
   - 🚀 **Scale testing** - Test với số users cao hơn (300, 500) để tìm breaking point
   - 💾 **Implement caching** - Có thể implement caching để giảm response time cho các requests phổ biến
   - ⚖️ **Load balancing** - Nếu cần xử lý nhiều users hơn, consider load balancing

---

## 📊 Performance Summary

| Metric | Value | Status | Notes |
|--------|-------|--------|-------|
| **Total Requests** | 11,276 | ✅ | Good volume |
| **Total Failures** | 0 (0.00%) | ✅ | Perfect! |
| **Average Response Time** | 731.62 ms | ⚠️ | Acceptable, có thể cải thiện |
| **Median Response Time** | 640 ms | ⚠️ | Acceptable |
| **95th Percentile** | 1,700 ms | ⚠️ | Cần cải thiện xuống < 1000ms |
| **99th Percentile** | 1,900 ms | ⚠️ | Cần investigate |
| **Min Response Time** | 15 ms | ✅ | Excellent |
| **Max Response Time** | 2,271 ms | ⚠️ | Cần investigate |
| **RPS** | 57.6 req/s | ✅ | Good throughput |
| **Concurrent Users** | 200 | ✅ | High load handled well |

---

## 📈 So Sánh Endpoints

| Metric | /v1/activities/suggest | /v1/conversations/end | Difference |
|--------|----------------------|----------------------|------------|
| **Requests** | 5,577 | 5,699 | +122 (2.2%) |
| **Failures** | 0 | 0 | Equal |
| **Avg Response Time** | 749.37 ms | 714.25 ms | +35.12 ms (4.7%) |
| **Median** | 690 ms | 590 ms | +100 ms (14.5%) |
| **95th Percentile** | 1,700 ms | 1,700 ms | Equal |
| **99th Percentile** | 1,900 ms | 1,900 ms | Equal |
| **Min** | 27 ms | 15 ms | +12 ms |
| **Max** | 2,268 ms | 2,271 ms | -3 ms |
| **RPS** | 29.4 req/s | 28.2 req/s | +1.2 req/s |
| **Avg Size** | 23,780 bytes | 3,998 bytes | +19,782 bytes (494%) |

**Nhận xét:**
- `/v1/activities/suggest` có response time trung bình cao hơn một chút (749ms vs 714ms)
- `/v1/activities/suggest` có response size lớn hơn nhiều (23.7KB vs 4KB) - điều này có thể giải thích response time cao hơn
- Cả 2 endpoints đều có 95th và 99th percentile giống nhau (1,700ms và 1,900ms)

---

## 🔍 Chi Tiết Kỹ Thuật

### Test Environment
- **Locust Version:** 2.42.6
- **OS:** Windows
- **Target Server:** http://103.253.20.30:30020
- **Concurrent Users:** 200
- **Test Status:** RUNNING (real-time test)

### Test Data
- **Conversation Logs:** Generated dynamically với 3-10 turns
- **User IDs:** Generated randomly với prefix "user_"
- **Bot Configuration:**
  - Bot ID: `talk_movie_preference`
  - Bot Type: `dd`

### Status Codes Accepted
- ✅ **200 OK** - Success
- ✅ **201 Created** - Success
- ✅ **202 Accepted** - Success (Async processing)

---

## 📝 Notes

- Test được chạy với **200 concurrent users** - đây là một load test khá cao
- **Zero failures** trong suốt quá trình test cho thấy API server rất ổn định
- Response time trung bình **731ms** là acceptable cho một API xử lý conversation logs phức tạp
- **95th percentile ở 1,700ms** cho thấy một số requests bị delay, có thể do:
  - Server processing time cho các conversation logs lớn
  - Database query time
  - Network latency
- **RPS 57.6** với 200 users cho thấy mỗi user gửi khoảng **0.29 requests/giây**, phù hợp với wait_time 1-3 giây

---

## 📎 Attachments

- Screenshot: Real-time Dashboard (1764649092830.png)
- Test đang chạy real-time tại thời điểm screenshot

---

**Report Generated:** 2025-12-02  
**Test Status:** RUNNING  
**Data Source:** Locust Real-time Dashboard
