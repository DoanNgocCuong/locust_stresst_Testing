# Robot Workflow – Locust Stress Test

Stress test suite cho Robot Workflow (initConversation + webhook) dựa trên thiết kế đã triển khai ở `3_ContextHandling_Robot`.

## Cấu trúc

```
src/
├── config.py              # Đọc cấu hình từ .env và constants
├── data_generators.py     # Sinh conversation_id, payloads, message pool
├── locustfile.py          # Locust tasks
├── README.md              # Tài liệu này
└── requirements.txt       # Dependencies
```

## Chuẩn bị môi trường

1. (Tuỳ chọn) tạo file `.env` tại `4_Robot_Workflow/.env` để override cấu hình:

```env
ROBOT_WORKFLOW_BASE_URL=http://103.253.20.30:30000
ROBOT_WORKFLOW_BOT_ID=3
ROBOT_WORKFLOW_WAIT_MIN=1
ROBOT_WORKFLOW_WAIT_MAX=3
ROBOT_WORKFLOW_WEIGHT_INIT=1
ROBOT_WORKFLOW_WEIGHT_WEBHOOK=3
ROBOT_WORKFLOW_MESSAGE_POOL=sẵn sàng|cho mình bài luyện tập tiếp theo|mình muốn kết thúc buổi học
```

2. Cài đặt dependency:

```bash
cd 4_Robot_Workflow/src
pip install -r requirements.txt
```

## Chạy Locust

### Web UI

```bash
locust -f locustfile.py --host=http://103.253.20.30:30000
```

Sau đó mở `http://localhost:8089`, nhập số user, spawn rate và chạy.

### Headless

```bash
locust -f locustfile.py --host=http://103.253.20.30:30000 --headless -u 50 -r 5 -t 5m
```

## Chi tiết task

- **Init conversation** (`/robot-ai-workflow/api/v1/bot/initConversation`):
  - Payload: `{ bot_id, conversation_id, input_slots }`
  - conversation_id được sinh ngẫu nhiên theo timestamp.
- **Webhook** (`/robot-ai-workflow/api/v1/bot/webhook`):
  - Payload: `{ conversation_id, message }`
  - message lấy ngẫu nhiên từ message pool (có thể cấu hình qua `.env`).
  - Nếu response có `status=END` → user tự động init conversation mới.

## Tuỳ chỉnh

- **Bot ID**: `ROBOT_WORKFLOW_BOT_ID`
- **Endpoint**: `ROBOT_WORKFLOW_INIT_ENDPOINT`, `ROBOT_WORKFLOW_WEBHOOK_ENDPOINT`
- **Wait time**: `ROBOT_WORKFLOW_WAIT_MIN`, `ROBOT_WORKFLOW_WAIT_MAX`
- **Tỷ lệ task**: `ROBOT_WORKFLOW_WEIGHT_INIT`, `ROBOT_WORKFLOW_WEIGHT_WEBHOOK`
- **Message pool**: `ROBOT_WORKFLOW_MESSAGE_POOL` (các message phân tách bằng `|`)

## Ghi chú

- Mặc định host là `103.253.20.30:30000` (robot-ai-workflow). Nếu test biến thể (9404) chỉ cần override base URL và endpoint trong `.env`.
- File `data/Simulation_Robot_ChildAgent/docs/ApiClientB.md` chứa mẫu payload thực tế, đã được phản ánh trong factory.
- Có thể mở rộng thêm data generators hoặc scripts (headless, report) tương tự `3_ContextHandling_Robot` nếu cần.

---

Đúng là ta đang test **2 API**:

1. `POST /robot-ai-workflow/api/v1/bot/initConversation`
2. `POST /robot-ai-workflow/api/v1/bot/webhook`

Cách hoạt động chuẩn trong Locust setup hiện tại:

- **Mỗi Locust user** đại diện cho một học viên mô phỏng.
- Khi user start (`on_start`), ta gọi **initConversation một lần** để lấy `conversation_id` riêng cho user đó.
- Sau đó user gửi message qua **webhook** nhiều lần, tái sử dụng cùng `conversation_id`.
- Nếu webhook trả trạng thái `END`, user sẽ init lại một conversation mới cho vòng lặp tiếp theo.

Nghĩa là:

- Không phải “mỗi API call đều init”.
- Chu trình chuẩn: **init** (1 lần) → **nhiều lần webhook**, giữ context.
- Chỉ khi nào conversation kết thúc hoặc lỗi thì user mới init lại.

---

# Bộ test stress Test

### Trả lời ngắn gọn

**Không bắt buộc**, tuỳ mục tiêu test:

---

### 1. Khi **không cần** câu real (trường hợp hiện tại)

Giữ như đang làm (câu fix sẵn + random) là đủ nếu mục tiêu là:

- **Đo tải hệ thống**: RPS, CPU, DB connection, latency, error rate.
- **Không quan trọng nội dung ngôn ngữ**, chỉ cần:
  - Payload đúng format (`conversation_id`, `message` là string).
  - Độ dài message “vừa phải”.

Ưu điểm:

- Đơn giản, dễ control.
- Ít rủi ro tạo ra case lạ làm lệch kết quả.
- Dễ tái lập (reproduce) test.

Với kiểu test “stress infra + flow API”, cách hiện tại **hoàn toàn chấp nhận được**.

---

### 2. Khi **nên** dùng câu user real

Nên dựng bộ câu real (hoặc lấy mẫu từ logs) nếu bạn muốn:

- Đánh giá **quality** / behavior của bot dưới tải (không chỉ performance).
- Muốn xem:
  - Tỉ lệ trả về `status=END` sớm do user nói sai format.
  - Bot có bị “lạc đề” với câu phức tạp không.
  - Các path hiếm trong workflow có được cover không.

Lúc đó có thể:

- Lấy 100–500 câu thực tế từ hệ thống / logs.
- Đưa vào `.env` hoặc 1 file JSON/CSV, rồi load làm `MESSAGE_POOL` để random.

---

### 3. Gợi ý thực tế cho bài này

- **Bước 1** (performance/stress): tiếp tục dùng **câu synthethic như hiện tại** để:
  - Khoanh vùng bottleneck (DB, max_connections, v.v.).
  - Xác định ngưỡng users (100/200/300…).
- **Bước 2** (behavior/quality – nếu cần): thêm 1 profile Locust khác hoặc 1 `MESSAGE_POOL` khác chứa **câu real** để:
  - Xem bot hành xử ra sao dưới tải tương tự.

Nếu mục tiêu của bạn chủ yếu là **“chịu được bao nhiêu users mà không gãy”** thì **chưa cần** dựng câu real; khi bắt đầu quan tâm đến **chất lượng phản hồi dưới tải**, lúc đó hãy đầu tư thêm bộ câu user thực.
