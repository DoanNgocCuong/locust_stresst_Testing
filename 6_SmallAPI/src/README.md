# Locust Stress Test cho Qwen3-1.7B API

## Mô tả

Locust test suite để stress test API `/v1/chat/completions` của Qwen3-1.7B model.

API này được sử dụng để detect emotion và learn_score từ user input trong format:
- Question: string
- Answer: string
- Response: string to check

## Cấu trúc thư mục

```
6_SmallAPI/
├── src/
│   ├── config.py              # Cấu hình cho test
│   ├── data_generators.py     # Generate test data
│   ├── locustfile.py          # Locust test class
│   ├── requirements.txt       # Dependencies
│   └── README.md              # File này
├── README_API_Qwen3_1.7B.md  # API documentation
└── .env                       # Environment variables (tùy chọn)
```

## Cài đặt

### 1. Cài đặt dependencies

```bash
cd 6_SmallAPI/src
pip install -r requirements.txt
```

### 2. Cấu hình (tùy chọn)

Tạo file `.env` ở thư mục `6_SmallAPI/` để override các giá trị mặc định:

```env
# Base URL của API server
QWEN_API_BASE_URL=http://124.197.20.86:7862

# API Endpoint
QWEN_API_CHAT_COMPLETIONS_ENDPOINT=/v1/chat/completions

# Model name
QWEN_API_MODEL_NAME=Qwen/Qwen3-1.7B

# API Parameters
QWEN_API_TEMPERATURE=0
QWEN_API_REPETITION_PENALTY=1.1
QWEN_API_STREAM=false
QWEN_API_ENABLE_THINKING=false

# Wait time giữa các requests (giây)
QWEN_API_WAIT_MIN=1.0
QWEN_API_WAIT_MAX=3.0
```

## Chạy test

### Chạy với Web UI (khuyến nghị)

```bash
cd 6_SmallAPI/src
locust
```

Sau đó mở browser tại: `http://localhost:8089`

### Chạy headless (không UI)

```bash
cd 6_SmallAPI/src
locust --headless -u 10 -r 2 -t 60s --host http://124.197.20.86:7862
```

**Giải thích tham số:**
- `--headless`: Chạy không có UI
- `-u 10`: Số lượng concurrent users
- `-r 2`: Spawn rate (users/second)
- `-t 60s`: Thời gian chạy test (60 giây)
- `--host`: Base URL của API server

### Chạy với file output

```bash
cd 6_SmallAPI/src
locust --headless -u 10 -r 2 -t 60s --host http://124.197.20.86:7862 --html report.html --csv results
```

## Cấu trúc code

### config.py

Chứa các cấu hình:
- Base URL và endpoints
- API parameters (temperature, repetition_penalty, etc.)
- System prompt
- Wait time giữa requests

### data_generators.py

Chứa các class để generate test data:
- `MessageFactory`: Sinh questions, answers, responses ngẫu nhiên
- `ChatCompletionPayloadFactory`: Tạo payload cho API
- `ChatCompletionPayload`: Dataclass chứa payload

### locustfile.py

Chứa Locust User class:
- `QwenAPIUser`: Class định nghĩa các task test
- `test_chat_completions`: Task gửi request tới API

## Test Data

Test data được generate ngẫu nhiên từ các danh sách mẫu:
- **SAMPLE_QUESTIONS**: 20 câu hỏi mẫu
- **SAMPLE_ANSWERS**: 20 câu trả lời mẫu
- **SAMPLE_RESPONSES**: 20 response mẫu

Mỗi request sẽ chọn ngẫu nhiên một bộ (question, answer, response) từ các danh sách này.

## Response Validation

Test sẽ validate response:
1. Status code phải là 200
2. Response phải là JSON hợp lệ
3. Response phải có field `choices` (theo format OpenAI API)

## Nguyên tắc thiết kế

Code tuân thủ **SOLID principles**:
- **Single Responsibility**: Mỗi module chỉ chịu trách nhiệm một việc
- **Open/Closed**: Dễ dàng mở rộng mà không cần sửa code cũ
- **Dependency Inversion**: Sử dụng dependency injection thông qua Config class

## Troubleshooting

### Lỗi kết nối

Nếu gặp lỗi kết nối, kiểm tra:
1. Base URL có đúng không?
2. API server có đang chạy không?
3. Firewall có chặn không?

### Lỗi response validation

Nếu response không pass validation:
1. Kiểm tra format response của API có đúng không?
2. Có thể cần điều chỉnh logic validation trong `_check_response_success()`

### Performance issues

Nếu test chạy chậm:
1. Giảm số lượng users (`-u`)
2. Tăng wait time giữa requests
3. Kiểm tra network latency

## Tài liệu tham khảo

- [Locust Documentation](https://docs.locust.io/)
- [Qwen3-1.7B API Documentation](../README_API_Qwen3_1.7B.md)

