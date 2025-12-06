# Hướng dẫn chạy Stress Test với dữ liệu từ Excel

## 📋 Tổng quan

Script này hỗ trợ chạy stress test với dữ liệu từ file Excel (cột `new_data`).
Dữ liệu sẽ được sử dụng làm content cho role `user` trong API request.

## 🔧 Chuẩn bị

### 1. Cài đặt dependencies

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\src
pip install -r requirements.txt
```

### 2. Tạo file Excel với cột `new_data`

Nếu chưa có file `result_all_rows.xlsx`, chạy script để tạo:

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\data
python generate_new_data.py --all
```

File sẽ được tạo tại: `6_SmallAPI/data/result_all_rows.xlsx`

## 🚀 Chạy Stress Test

### Cách 1: Sử dụng file Excel mặc định

File mặc định: `6_SmallAPI/data/result_all_rows.xlsx`

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\src
.\run_test.ps1 10 2 60s headless
```

### Cách 2: Chỉ định file Excel tùy chỉnh

Tạo file `.env` trong thư mục `6_SmallAPI`:

```env
EXCEL_DATA_PATH=D:\GIT\locust_stresst_Testing\6_SmallAPI\data\result_all_rows.xlsx
QWEN_API_BASE_URL=http://124.197.20.86:7862
```

Sau đó chạy:

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\src
.\run_test.ps1 10 2 60s headless
```

### Cách 3: Chạy với Web UI

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\src
.\run_test.ps1 10 2 60s
```

Mở browser tại: http://localhost:8089

## 📊 Format dữ liệu

File Excel phải có cột `new_data` với format:

```
Previous Question: Tớ buồn quá.
Previous Answer: i think a yummy
Response to check: Nghe vui quá! Bể Hả, cậu có muốn chơi trò kể tên các loại trái cây bằng tiếng Anh không? Name fruits in English!
```

Dữ liệu này sẽ được sử dụng trực tiếp làm `content` cho role `user`:

```json
{
    "role": "user",
    "content": "Previous Question: ...\nPrevious Answer: ...\nResponse to check: ..."
}
```

## 🔍 Kiểm tra dữ liệu

Script sẽ tự động:
- ✅ Load dữ liệu từ file Excel
- ✅ Lọc các dòng hợp lệ (không rỗng)
- ✅ Chọn ngẫu nhiên một dòng cho mỗi request
- ⚠️ Nếu không tìm thấy file Excel, sẽ fallback về dữ liệu mẫu

## 📝 Cấu hình

### Biến môi trường (.env)

```env
# Đường dẫn file Excel
EXCEL_DATA_PATH=D:\GIT\locust_stresst_Testing\6_SmallAPI\data\result_all_rows.xlsx

# API Configuration
QWEN_API_BASE_URL=http://124.197.20.86:7862
QWEN_API_CHAT_COMPLETIONS_ENDPOINT=/v1/chat/completions
QWEN_API_MODEL_NAME=Qwen/Qwen3-1.7B
QWEN_API_TEMPERATURE=0.0
QWEN_API_REPETITION_PENALTY=1.1
QWEN_API_STREAM=false
QWEN_API_ENABLE_THINKING=false

# Wait time giữa requests (giây)
QWEN_API_WAIT_MIN=1.0
QWEN_API_WAIT_MAX=3.0
```

## 🎯 Ví dụ Request

Mỗi request sẽ có format:

```json
{
    "model": "Qwen/Qwen3-1.7B",
    "messages": [
        {
            "role": "system",
            "content": "You are now intention detection..."
        },
        {
            "role": "user",
            "content": "Previous Question: Tớ buồn quá.\nPrevious Answer: i think a yummy\nResponse to check: Nghe vui quá! Bể Hả, cậu có muốn chơi trò kể tên các loại trái cây bằng tiếng Anh không? Name fruits in English!"
        }
    ],
    "temperature": 0.0,
    "repetition_penalty": 1.1,
    "stream": false,
    "enable_thinking": false
}
```

## ⚠️ Troubleshooting

### Lỗi: File Excel không tồn tại

```
⚠️  User QwenAPIUser: File Excel không tồn tại: ...
```

**Giải pháp:** Chạy script `generate_new_data.py --all` để tạo file Excel.

### Lỗi: Không có cột 'new_data'

```
ValueError: File Excel không có cột 'new_data'
```

**Giải pháp:** Đảm bảo file Excel có cột `new_data` hoặc chạy lại script `generate_new_data.py`.

### Fallback về dữ liệu mẫu

Nếu không load được Excel, script sẽ tự động sử dụng dữ liệu mẫu từ `SAMPLE_QUESTIONS`, `SAMPLE_ANSWERS`, `SAMPLE_RESPONSES`.

## 📈 Kết quả

Sau khi chạy, bạn sẽ có:
- HTML report: `6_SmallAPI/results/report_YYYYMMDD_HHMMSS.html`
- CSV files: `6_SmallAPI/results/results_YYYYMMDD_HHMMSS_*.csv`

