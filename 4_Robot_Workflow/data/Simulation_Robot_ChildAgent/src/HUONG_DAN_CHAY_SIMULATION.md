# Hướng Dẫn Chạy Simulation và Xuất Kết Quả Ra Excel

## 📋 Yêu Cầu

1. Python 3.8+
2. Cài đặt các thư viện cần thiết
3. File `.env` với các biến môi trường cần thiết

## 🚀 Các Bước Chạy

### Bước 1: Cài đặt Dependencies

```bash
cd data/Simulation_Robot_ChildAgent/src
pip install -r requirements.txt
```

### Bước 2: Cấu Hình Environment Variables

Tạo file `.env` trong thư mục `src` với nội dung:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Bước 3: Chạy Simulation

#### **Option 1: Chạy 1 Simulation**

```bash
python run_simulation.py
```

#### **Option 2: Chạy Nhiều Simulation (2 hoặc nhiều hơn)**

```bash
python run_multiple_simulations.py
```

### Bước 4: Nhập Thông Tin

Khi chạy, chương trình sẽ yêu cầu:
- **Số lượt tối đa**: Nhập số lượt hội thoại muốn chạy (ví dụ: 5, 10, 20)
- **Số lượng simulation**: (Chỉ với `run_multiple_simulations.py`) Nhập số simulation muốn chạy (ví dụ: 2)
- **Bot ID**: (Chỉ với `run_multiple_simulations.py`) Nhập Bot ID (ví dụ: 177)

### Bước 5: Kết Quả

Sau khi chạy xong, file Excel sẽ được lưu trong thư mục `results/` với tên:
- `simulation_results_YYYYMMDD_HHMMSS.xlsx` (cho 1 simulation)
- `simulation_1_YYYYMMDD_HHMMSS.xlsx`, `simulation_2_YYYYMMDD_HHMMSS.xlsx`, ... (cho nhiều simulation)

## 📊 Cấu Trúc File Excel

File Excel có **1 sheet** với **4 cột**:

### 1. **Role**
- RoleA: Vai trò học sinh (sử dụng OpenAI API)
- RoleB: Vai trò giáo viên (sử dụng Robot API)

### 2. **curl API**
- **RoleA**: 
  - "Initial message" (cho tin nhắn đầu tiên)
  - "OpenAI API (Chat Completion)" (cho các tin nhắn sau)
- **RoleB**: 
  - cURL command để gọi API webhook
  - Ví dụ: `curl -X POST "http://103.253.20.30:9404/robot-ai-lesson/api/v1/bot/webhook" -H "Content-Type: application/json" -d '{"conversation_id": "...", "message": "..."}'`

### 3. **Output**
- Nội dung tin nhắn từ RoleA hoặc RoleB

### 4. **Response time**
- Thời gian phản hồi tính bằng giây (6 chữ số thập phân)

## ⚙️ Tùy Chỉnh

### Thay đổi Bot ID

Sửa trong file `run_simulation.py`:

```python
bot_id = 177  # Thay đổi ID bot ở đây
```

### Thay đổi Prompt

Sửa trong file `run_simulation.py`, phần `roleA_prompt`:

```python
roleA_prompt = """
TITLE: Role-Play: Cuong's Interactive Learning Adventure
...
"""
```

### Thay đổi Initial Message

Sửa trong file `run_simulation.py`:

```python
initial_history = [{"role": "roleA", "content": "sẵn sàng"}]  # Thay đổi message ban đầu
```

## 🔍 Xử Lý Lỗi

### Lỗi: ModuleNotFoundError

```bash
pip install -r requirements.txt
```

### Lỗi: OPENAI_API_KEY not found

Kiểm tra file `.env` có đúng định dạng và có API key chưa.

### Lỗi: Cannot connect to API

Kiểm tra:
- Kết nối internet
- API_BASE_URL trong file `.env`
- Bot ID có đúng không

## 📝 Ghi Chú

- File Excel được lưu tự động với timestamp
- Thư mục `results/` sẽ được tạo tự động nếu chưa có
- Mỗi lần chạy sẽ tạo file Excel mới
- File Excel có thể mở bằng Microsoft Excel, Google Sheets, hoặc LibreOffice

## 🎯 Ví Dụ Sử Dụng

```bash
# Chạy simulation với 5 lượt
python run_simulation.py
# Nhập: 5

# Kết quả sẽ được lưu tại:
# results/simulation_results_20250115_143022.xlsx
```

## 📞 Hỗ Trợ

Nếu gặp vấn đề, kiểm tra:
1. Log trong console
2. File log trong thư mục `logs/` (nếu có)
3. File Excel có được tạo thành công không

