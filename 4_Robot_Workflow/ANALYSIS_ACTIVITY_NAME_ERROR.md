# Phân Tích Lỗi: "Lỗi lấy tên bài học hiện tại cho LLM - Content not found"

## 1. VẤN ĐỀ

Khi chạy Locust stress test, xuất hiện lỗi:

```
Thông tin: Lỗi lấy tên bài học hiện tại cho LLM, conversation_id: conv_doanngoccuong_locustTest_1764906692799_572, error: Content not found. Type: hội thoại LLM - id: conv_doanngoccuong_locustTest_1764906692799_572
```

**Đặc điểm:**
- Lỗi xuất hiện với các `conversation_id` mới được tạo trong Locust test
- Format conversation_id: `conv_doanngoccuong_locustTest_{timestamp}_{random}`
- Lỗi đến từ phía backend server, không phải từ code Locust test

---

## 2. NGUYÊN NHÂN

### 2.1. Luồng xử lý khi gọi API `initConversation`

Khi Locust test gọi API:
```bash
POST /robot-ai-workflow/api/v1/bot/initConversation
```

Backend server sẽ **tự động gọi 2 API external**:

#### API 1: `user_profile`
```bash
GET https://robot-api.hacknao.edu.vn/robot/api/v1/llm/user_profile
  ?conversation_id={conversation_id}
  &token={token}
```

#### API 2: `activity_name` ⚠️ (Đây là nguồn gốc lỗi)
```bash
GET https://robot-api.hacknao.edu.vn/robot/api/v1/llm/activity_name
  ?conversation_id={conversation_id}
  &token={token}
```

### 2.2. Nguyên nhân gốc rễ

1. **Conversation_id chưa tồn tại trong hệ thống bên ngoài:**
   - Locust test tạo `conversation_id` mới ngẫu nhiên
   - `conversation_id` này chưa được đăng ký trong hệ thống `robot-api.hacknao.edu.vn`
   - API `activity_name` yêu cầu `conversation_id` phải đã tồn tại và có dữ liệu liên quan

2. **Thiếu dữ liệu context:**
   - API `activity_name` cần biết "bài học hiện tại" của user
   - Với `conversation_id` mới, hệ thống chưa có thông tin về bài học đang học
   - → Trả về "Content not found"

3. **Backend không xử lý graceful:**
   - Backend có thể không có cơ chế fallback khi API external trả về lỗi
   - Hoặc có xử lý nhưng vẫn log warning/error

---

## 3. GIẢI PHÁP

### 3.1. Giải pháp ngắn hạn (Không cần sửa code)

**Nếu lỗi này không ảnh hưởng đến kết quả test:**
- Lỗi này có thể là **expected behavior** khi test với conversation_id mới
- Backend có thể đã xử lý fallback và vẫn tiếp tục xử lý request
- **Hành động:** Bỏ qua warning này nếu:
  - API `initConversation` vẫn trả về status 200
  - Test vẫn chạy bình thường
  - Chỉ là log warning, không phải error

### 3.2. Giải pháp trung hạn (Sửa phía Backend - Khuyến nghị)

**Backend nên xử lý graceful khi API external fail:**

```python
# Pseudocode cho backend
try:
    activity_name = call_external_api_activity_name(conversation_id)
except ContentNotFoundError:
    # Fallback: Sử dụng giá trị mặc định hoặc bỏ qua
    activity_name = None  # hoặc "Bài học mới"
    log_warning(f"Activity name not found for {conversation_id}, using default")
```

**Lợi ích:**
- Test có thể chạy với conversation_id mới
- Không cần setup dữ liệu trước
- Phù hợp với stress test scenario

### 3.3. Giải pháp dài hạn (Cải thiện test data)

**Option A: Pre-register conversation_id**
- Trước khi chạy test, tạo sẵn conversation_id trong hệ thống bên ngoài
- Phức tạp hơn, cần thêm script setup

**Option B: Mock external API trong test environment**
- Tạo mock server cho API `activity_name`
- Trả về dữ liệu giả lập
- Phù hợp cho integration test

**Option C: Sử dụng conversation_id thật từ production**
- Export danh sách conversation_id có sẵn
- Sử dụng trong test
- ⚠️ Cần cẩn thận với dữ liệu production

---

## 4. KIỂM TRA VÀ XÁC NHẬN

### 4.1. Kiểm tra xem lỗi có ảnh hưởng không:

```bash
# Chạy test và kiểm tra:
1. API initConversation có trả về 200 không?
2. Test có tiếp tục chạy sau lỗi không?
3. Có request nào bị fail do lỗi này không?
```

### 4.2. Test thủ công API activity_name:

```bash
curl --location -G 'https://robot-api.hacknao.edu.vn/robot/api/v1/llm/activity_name' \
  --data-urlencode 'conversation_id=conv_doanngoccuong_locustTest_1764906692799_572' \
  --data-urlencode 'token=b1812cb7-2513-408b-bb22-d9f91b099fbd' \
  --header 'Accept: application/json'
```

**Kết quả mong đợi:**
- Nếu conversation_id chưa tồn tại → "Content not found" (expected)
- Nếu conversation_id đã tồn tại → Trả về tên bài học

---

## 5. KHUYẾN NGHỊ

### ✅ Nên làm:
1. **Xác nhận với team Backend:** Lỗi này có ảnh hưởng đến business logic không?
2. **Kiểm tra response của initConversation:** Có thành công không dù có warning?
3. **Document hóa:** Ghi chú rằng đây là expected behavior khi test với conversation_id mới

### ⚠️ Cần cân nhắc:
- Nếu lỗi này làm fail request → Cần fix backend ngay
- Nếu chỉ là warning → Có thể bỏ qua trong stress test

### ❌ Không nên:
- Tạo conversation_id thật trong production chỉ để test
- Bỏ qua nếu lỗi này làm ảnh hưởng đến kết quả test

---

## 6. TÀI LIỆU THAM KHẢO

- File: `4_Robot_Workflow/result/.md` - Mô tả về API external
- File: `4_Robot_Workflow/src/locustfile.py` - Code Locust test
- File: `4_Robot_Workflow/src/data_generators.py` - Logic tạo conversation_id

---

**Ngày tạo:** 2025-01-XX  
**Người phân tích:** AI Assistant  
**Trạng thái:** Đang chờ xác nhận từ team Backend



