# SQL Stress Test – Query trên bảng `llm_bot`

Stress test cho câu SQL:

```sql
SELECT id,
       name,
       description,
       task_chain,
       generation_params,
       provider_name,
       system_prompt,
       format_output
FROM llm_bot
WHERE id = 373;
```

## Cấu trúc thư mục

```text
5_SQLQuery/src/
├── config.py        # Đọc cấu hình DB & câu SQL từ .env
├── db_client.py     # Client PostgreSQL, execute query
├── locustfile.py    # Locust User cho stress test SQL
├── requirements.txt # Dependencies
└── README.md        # Tài liệu này
```

## Cấu hình

### 1. Thêm vào `.env` (ở root project hoặc riêng cho 5_SQLQuery)

```env
# PostgreSQL connection
SQL_DB_HOST=127.0.0.1
SQL_DB_PORT=5432
SQL_DB_NAME=your_db_name
SQL_DB_USER=your_db_user
SQL_DB_PASSWORD=your_db_password

# Optional
SQL_DB_CONNECT_TIMEOUT=5

# Optional override câu query (nếu khác với mặc định)
# SQL_STRESS_QUERY=SELECT ... FROM llm_bot WHERE id = 373;
```

> Lưu ý: mặc định query đã lấy từ file `sql.md`, chỉ cần override nếu bạn muốn đổi điều kiện WHERE.

### 2. Cài đặt dependencies

```bash
cd 5_SQLQuery/src
pip install -r requirements.txt
```

## Chạy stress test

### Web UI mode

```bash
locust -f locustfile.py
```

Sau đó mở `http://localhost:8089`, nhập:
- Number of users (vd: 50, 100, 200)
- Spawn rate (vd: 5, 10)

Locust sẽ hiển thị:
- Request type: `SQL`
- Name: `SELECT llm_bot WHERE id = 373`
- Metrics: requests/s, avg, median, p95, p99, failures…

### Headless mode (không UI)

```bash
locust -f locustfile.py \
  --headless \
  -u 100 -r 10 -t 2m \
  --csv=results/sql_stress
```

File kết quả CSV sẽ nằm trong `results/sql_stress_*.csv`.

## Cách hoạt động

- Mỗi `SqlUser`:
  - Khi `on_start`:
    - Mở **1 connection** tới PostgreSQL bằng `psycopg2`.
  - Task `run_select_llm_bot`:
    - Thực thi câu SELECT được cấu hình.
    - Đo thời gian thực thi (`duration_ms`).
    - Gửi kết quả vào Locust bằng `events.request_success`.
  - Khi `on_stop`:
    - Đóng connection.

Như vậy:
- **Mỗi user = 1 connection**, gửi query lặp lại trong suốt thời gian test.
- Bạn có thể tăng `u` (users) để tăng số connection đồng thời & số query/giây.

## Tuỳ chỉnh

- **Query khác**: set `SQL_STRESS_QUERY` trong `.env`.
- **Wait time** giữa 2 lần query:
  - Sửa trong `locustfile.py`:
    ```python
    wait_time = between(0.1, 0.5)
    ```
  - Có thể cho về `between(0, 0)` nếu muốn bắn tối đa.

## Ghi chú

- Đây là stress test **trực tiếp tới DB**, không qua HTTP API.
- Hãy đảm bảo:
  - User DB dùng cho test có quyền `SELECT` trên bảng `llm_bot`.
  - `max_connections` của PostgreSQL đủ lớn so với `u` (số users) bạn đặt.







