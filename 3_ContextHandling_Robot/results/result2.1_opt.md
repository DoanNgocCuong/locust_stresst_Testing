```bash
mình đã tăng trong .env với @.env (87-89) DB


DB_POOL_SIZE=100              # Base connection pool size (default: 50)
DB_MAX_OVERFLOW=200          # Max overflow connections (default: 100, total max = 150)
# DB_POOL_TIMEOUT=30           # Timeout in seconds when waiting for connection (default: 30)
# DB_POOL_RECYCLE=3600         # Recycle connections after N seconds (default: 3600 = 1 hour)
 



đã tăng như này rồi vẫn bị ý 
```



Đang kiểm tra tại sao tăng pool size trong .env vẫn không hiệu quả:

[5 tools called]

Đang kiểm tra các nguyên nhân khác tại sao tăng pool size vẫn không hiệu quả:

[4 tools called]

Đã tăng pool size trong `.env` nhưng vẫn bị. Dưới đây là các nguyên nhân có thể:

## Phân tích: Tại sao tăng pool size vẫn bị?

### Nguyên nhân 1: Service chưa restart (khả năng cao)

Khi thay đổi `.env`, cần restart service để load giá trị mới:

```
Application startup:
├─ Load .env file → Settings object created
├─ Database engine created với pool_size từ settings
└─ Engine object được cache → Không tự động reload khi .env thay đổi
```

Giải pháp:

- Restart API service (FastAPI)
- Restart Worker service (RabbitMQ consumer)

---

### Nguyên nhân 2: PostgreSQL max_connections limit (khả năng rất cao)

PostgreSQL có giới hạn `max_connections` (mặc định thường là 100-200). Nếu bạn cấu hình 300 connections (100 + 200) nhưng PostgreSQL chỉ cho phép 100 → sẽ bị giới hạn.

Kiểm tra:

```sql
-- Kết nối vào PostgreSQL
SELECT name, setting, unit 
FROM pg_settings 
WHERE name = 'max_connections';

-- Xem số connections đang dùng
SELECT count(*) as active_connections 
FROM pg_stat_activity;
```

Nếu `max_connections = 100` nhưng bạn cần 300 → phải tăng PostgreSQL limit:

```sql
-- Trong postgresql.conf
max_connections = 500  # Tăng lên 500

-- Hoặc trong .env (nếu dùng Docker)
POSTGRES_MAX_CONNECTIONS=500
```

---

### Nguyên nhân 3: RabbitMQ prefetch_count = 1 (bottleneck)

```python
# src/app/background/rabbitmq_consumer.py:150
self.channel.basic_qos(prefetch_count=1)  # ⚠️ CHỈ 1 message/worker
```

Với `prefetch_count=1`:

- Mỗi worker chỉ xử lý 1 message tại một thời điểm
- Worker phải đợi message xong mới lấy message tiếp
- Với 200 requests → queue backlog → latency tăng

Giải pháp: Tăng `prefetch_count`:

```python
self.channel.basic_qos(prefetch_count=10)  # Xử lý 10 messages đồng thời
```

---

### Nguyên nhân 4: Redis single connection (bottleneck)

Nếu code dùng Redis cache và chỉ có 1 connection (singleton) → tất cả requests phải chờ nhau.

---

### Cách kiểm tra và xử lý

#### Bước 1: Verify giá trị đang được dùng

Thêm log để xem giá trị thực tế:

```python
# src/app/db/database_connection.py
logger.info(
    f"🔧 Database Pool Configuration:\n"
    f"   - pool_size: {settings.DB_POOL_SIZE}\n"
    f"   - max_overflow: {settings.DB_MAX_OVERFLOW}\n"
    f"   - Total max connections: {settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW}\n"
    f"   - pool_timeout: {settings.DB_POOL_TIMEOUT}s"
)
```

Sau khi restart, kiểm tra log:

```
🔧 Database Pool Configuration:
   - pool_size: 100  ← Phải là 100 (không phải 50)
   - max_overflow: 200  ← Phải là 200 (không phải 100)
   - Total max connections: 300
```

Nếu vẫn thấy giá trị cũ → chưa restart hoặc `.env` chưa được load.

---

#### Bước 2: Kiểm tra PostgreSQL max_connections

```bash
# Kết nối vào PostgreSQL
psql -U postgres -d context_handling_db

# Check max_connections
SELECT name, setting FROM pg_settings WHERE name = 'max_connections';

# Check active connections
SELECT count(*) as active, 
       (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') as max_conns,
       (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') - count(*) as available
FROM pg_stat_activity;
```

Nếu `max_connections < 300` → phải tăng PostgreSQL limit.

---

#### Bước 3: Tăng RabbitMQ prefetch_count

```python
# src/app/background/rabbitmq_consumer.py:150
# Tăng từ 1 lên 10
self.channel.basic_qos(prefetch_count=10)
```

---

### Tóm tắt checklist

- [ ] Đã restart API service sau khi đổi `.env`?
- [ ] Đã restart Worker service sau khi đổi `.env`?
- [ ] PostgreSQL `max_connections` >= 300?
- [ ] RabbitMQ `prefetch_count` đã tăng từ 1 lên 10?
- [ ] Redis có connection pool (không phải singleton)?

---

### Khuyến nghị ngay

1. Tăng PostgreSQL max_connections:

```bash
# Kiểm tra file config
# Linux: /etc/postgresql/*/main/postgresql.conf
# Docker: environment variable POSTGRES_MAX_CONNECTIONS=500

# Sau khi set, restart PostgreSQL
```

2. Tăng RabbitMQ prefetch_count:

```python
# src/app/background/rabbitmq_consumer.py
self.channel.basic_qos(prefetch_count=10)  # Từ 1 → 10
```

3. Verify giá trị trong log:

Sau khi restart, kiểm tra log để đảm bảo pool size = 100 + 200 = 300.

Bạn muốn tôi tạo script để check các giá trị này không?
