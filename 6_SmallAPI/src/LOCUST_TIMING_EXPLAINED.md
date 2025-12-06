# ⏱️ Locust Response Time - Giải Thích Chi Tiết

## ✅ Câu Trả Lời Ngắn Gọn

**Locust CHỈ đo thời gian từ khi bắt đầu gửi request đến khi nhận được response từ API.**

## 📊 Cách Locust Đo Thời Gian

### 1. Thời gian được tính (Response Time)

Locust chỉ đo thời gian trong context của `self.client.post()`:

```python
with self.client.post(...) as response:
    # ⏱️ Locust đo thời gian từ đây đến khi response về
    # Thời gian này = Network latency + Server processing time
    pass
```

**Response Time = Thời gian từ khi gửi request đến khi nhận được response**

### 2. Thời gian KHÔNG được tính

#### a) Code chạy TRƯỚC `self.client.post()`

```python
@task
def test_chat_completions(self):
    # ❌ KHÔNG tính vào response time
    payload = self.payload_factory.build_payload()  # Tạo payload
    
    # ✅ Bắt đầu đo từ đây
    with self.client.post(...) as response:
        pass
```

**Ví dụ:**
- `build_payload()` - Tạo payload (vài ms) → **KHÔNG tính**
- `get_random_new_data()` - Lấy data từ Excel (vài ms) → **KHÔNG tính**
- `payload.to_dict()` - Convert sang dict (vài ms) → **KHÔNG tính**

#### b) Code trong `on_start()`

```python
def on_start(self):
    # ❌ KHÔNG tính vào response time
    self.payload_factory = ChatCompletionPayloadFactory(...)
```

**Ví dụ:**
- Load Excel data → **KHÔNG tính** (đã được tối ưu load 1 lần)
- Khởi tạo factory → **KHÔNG tính**

#### c) Code chạy SAU khi response về (nhưng vẫn trong context)

```python
with self.client.post(...) as response:
    # ⚠️ Có thể tính một chút (nhưng rất nhỏ, thường < 1ms)
    data = response.json()  # Parse JSON
    self._check_response_success(response)  # Validate
```

**Lưu ý:** 
- Locust đã nhận được response rồi, nên thời gian parse/validate **rất nhỏ** (< 1ms)
- Thời gian này **không đáng kể** so với network + server processing time

## 🔍 Code Hiện Tại

### Phân tích từng bước:

```python
@task
def test_chat_completions(self):
    # Bước 1: Tạo payload (TRƯỚC khi gửi request)
    # ⏱️ Thời gian: ~1-5ms (tùy vào việc lấy data từ Excel)
    # ❌ KHÔNG tính vào response time
    payload = self.payload_factory.build_payload()
    
    # Bước 2: Gửi request và đo thời gian
    # ⏱️ Bắt đầu đo từ đây
    with self.client.post(
        Config.CHAT_COMPLETIONS_ENDPOINT,
        json=payload.to_dict(),  # Convert (rất nhanh, < 1ms)
        headers=Config.DEFAULT_HEADERS,
        catch_response=True,
        name="POST /v1/chat/completions",
    ) as response:
        # ⏱️ Locust đo đến khi response về (network + server time)
        # ✅ Đây là response time thực sự
        
        # Bước 3: Validate response (SAU khi nhận được response)
        # ⏱️ Thời gian: ~0.5-2ms (parse JSON + validate)
        # ⚠️ Có tính một chút, nhưng không đáng kể
        self._check_response_success(response)
```

## 📈 Response Time Breakdown

```
Total Response Time (Locust đo) = Network Time + Server Processing Time + Parse Time (rất nhỏ)

Ví dụ:
- Network latency: 50ms
- Server processing: 200ms
- Parse JSON: 1ms
→ Total: 251ms (Locust báo)
```

**Lưu ý:** Parse time (1ms) rất nhỏ so với server time (200ms), nên có thể bỏ qua.

## ✅ Kết Luận

1. **Locust CHỈ đo response time từ API** (network + server processing)
2. **Thời gian tạo payload KHÔNG tính** (chạy trước khi gửi request)
3. **Thời gian validate response CÓ tính một chút** (nhưng rất nhỏ, < 1ms)
4. **Thời gian load Excel KHÔNG tính** (đã được tối ưu load 1 lần trước khi test)

## 🎯 Response Time trong Locust Dashboard

Khi bạn xem Locust dashboard, các metrics sau đều là **response time từ API**:

- **Average Response Time**: Trung bình thời gian response
- **Min/Max Response Time**: Min/Max thời gian response
- **95th/99th percentile**: 95%/99% requests có response time ≤ giá trị này

**Tất cả đều đo từ khi gửi request đến khi nhận được response từ server.**

