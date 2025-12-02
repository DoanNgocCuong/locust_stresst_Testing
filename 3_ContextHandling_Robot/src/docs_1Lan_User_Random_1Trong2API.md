Đang kiểm tra cách test hiện tại:

[3 tools called]

Phân tích cách test hiện tại:

[1 tool called]

## Phân tích: Cách test hiện tại

### Cách test hiện tại hoạt động

Từ code, cách test hiện tại:

```python
@task(Config.WEIGHT_CONVERSATION_END)  # weight = 1
def test_conversation_end(self):
    # Gửi request đến /v1/conversations/end

@task(Config.WEIGHT_ACTIVITIES_SUGGEST)  # weight = 1  
def test_activities_suggest(self):
    # Gửi request đến /v1/activities/suggest

wait_time = between(1, 3)  # Đợi 1-3 giây giữa các task
```

Cách hoạt động:

- Không phải “1 lúc bắn 2 API” cùng lúc từ 1 user
- Mỗi user chạy tuần tự: chọn 1 task (theo weight) → gửi request → đợi 1-3s → chọn task tiếp theo
- Với 200 users, nhiều users có thể chạy các task khác nhau cùng lúc

Ví dụ với 1 user:

```
User 1: 
  → Chọn task (50% chance mỗi task)
  → Gửi POST /v1/conversations/end
  → Đợi 2 giây
  → Chọn task tiếp theo
  → Gửi POST /v1/activities/suggest
  → Đợi 1.5 giây
  → Lặp lại...
```

Với 200 users:

- Khoảng 100 users đang gọi `/v1/conversations/end`
- Khoảng 100 users đang gọi `/v1/activities/suggest`
- Tổng RPS ~57.6 (29.4 + 28.2)

---

## Có chuẩn không?

### So sánh với real-world usage

#### Scenario 1: Real-world usage pattern

```
User flow thực tế:
1. User bắt đầu conversation → Gọi nhiều APIs khác
2. User kết thúc conversation → Gọi /v1/conversations/end
3. User muốn xem suggestions → Gọi /v1/activities/suggest

→ 2 APIs này KHÔNG được gọi cùng lúc bởi 1 user
→ Nhưng có thể được gọi bởi nhiều users khác nhau cùng lúc
```

#### Scenario 2: Test hiện tại

```
Test pattern:
- Mỗi user có 50% chance gọi mỗi API
- Các users gọi ngẫu nhiên, không theo flow thực tế
- 2 APIs được gọi song song bởi nhiều users khác nhau
```

---

## Đánh giá

### Điểm tốt

1. Phản ánh load thực tế: nhiều users gọi các API khác nhau cùng lúc
2. Test được cả 2 endpoints dưới cùng điều kiện load
3. Weight 1:1 phù hợp nếu 2 API có tần suất sử dụng tương đương

### Điểm cần xem xét

1. Không theo user flow thực tế: trong thực tế, 1 user không gọi 2 API này ngẫu nhiên
2. Weight 1:1 có thể không phản ánh đúng tỷ lệ thực tế
3. Khó phân tích riêng performance của từng API khi có vấn đề

---

## Khuyến nghị

### Option 1: Test riêng từng API (isolated testing) — khuyến nghị cho performance testing

Ưu điểm:

- Dễ xác định bottleneck của từng API
- Dễ so sánh performance
- Phù hợp để tìm breaking point của từng endpoint

Nhược điểm:

- Không phản ánh load thực tế (nhiều APIs cùng lúc)

Khi nào dùng:

- Performance testing
- Tìm breaking point
- Debug performance issues

### Option 2: Test cả 2 cùng lúc (mixed load) — khuyến nghị cho load testing

Ưu điểm:

- Phản ánh load thực tế hơn
- Test được resource contention
- Phù hợp để validate production readiness

Nhược điểm:

- Khó phân tích riêng từng API
- Cần điều chỉnh weight cho đúng tỷ lệ thực tế

Khi nào dùng:

- Load testing
- Capacity planning
- Production validation

### Option 3: Test theo user flow (realistic scenario) — khuyến nghị cho end-to-end testing

```python
@task(1)
def user_flow(self):
    # 1. Start conversation (nếu cần)
    # 2. Gọi /v1/activities/suggest
    # 3. Sau một lúc, gọi /v1/conversations/end
    # → Mô phỏng user flow thực tế
```

Ưu điểm:

- Mô phỏng user flow thực tế
- Test được dependencies giữa các APIs

Nhược điểm:

- Phức tạp hơn
- Khó control tỷ lệ load

---

## Kết luận và khuyến nghị

### Cách test hiện tại

- Không sai, nhưng chưa tối ưu
- Phù hợp cho mixed load testing
- Cần điều chỉnh weight nếu tỷ lệ thực tế khác 1:1

### Khuyến nghị

1. Giữ cách test hiện tại cho mixed load testing
2. Thêm test riêng từng API để so sánh performance
3. Điều chỉnh weight dựa trên tỷ lệ thực tế:

   ```python
   # Nếu trong thực tế:
   # - /v1/conversations/end được gọi 70% thời gian
   # - /v1/activities/suggest được gọi 30% thời gian

   WEIGHT_CONVERSATION_END = 7
   WEIGHT_ACTIVITIES_SUGGEST = 3
   ```
4. Cân nhắc thêm test theo user flow nếu cần end-to-end testing

---

## Tóm tắt

- Cách test hiện tại: không phải “1 lúc bắn 2 API” từ 1 user, mà là nhiều users gọi các API khác nhau cùng lúc
- Có chuẩn không: chuẩn cho mixed load testing, nhưng nên bổ sung isolated testing và điều chỉnh weight theo tỷ lệ thực tế
- Khuyến nghị: giữ mixed load, thêm isolated testing, và điều chỉnh weight theo production metrics

Cách test hiện tại hợp lý cho load testing, nhưng nên bổ sung isolated testing để phân tích sâu hơn.
