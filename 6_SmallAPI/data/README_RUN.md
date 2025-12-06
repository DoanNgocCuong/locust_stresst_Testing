# Hướng dẫn chạy script generate_new_data.py

## Cài đặt dependencies

```bash
cd 6_SmallAPI/data
pip install -r requirements.txt
```

## Các lệnh chạy

### 1. Chạy 5 dòng đầu (mặc định)

```bash
cd 6_SmallAPI/data
python generate_new_data.py
```

Hoặc chỉ định rõ số dòng:

```bash
python generate_new_data.py --sample 5
```

### 2. Chạy hàng loạt (toàn bộ file)

```bash
cd 6_SmallAPI/data
python generate_new_data.py --all
```

### 3. Chỉ định file đầu vào/đầu ra

```bash
# Chỉ định file đầu vào
python generate_new_data.py --sample 10 --input "path/to/input.xlsx"

# Chỉ định file đầu ra
python generate_new_data.py --all --output "path/to/output.xlsx"

# Cả hai
python generate_new_data.py --sample 5 --input "input.xlsx" --output "output.xlsx"
```

## Kết quả

- **Chạy 5 dòng**: File kết quả sẽ là `result_sample_5_rows.xlsx`
- **Chạy toàn bộ**: File kết quả sẽ là `result_all_rows.xlsx`
- **Tùy chỉnh**: File kết quả theo tên bạn chỉ định

## Ví dụ output

```
Đang đọc file: D:\GIT\locust_stresst_Testing\6_SmallAPI\data\data_for_stressTest.xlsx

Tổng số dòng trong file: 5949
Các cột trong file: ['conversationID', 'BOT_RESPONSE_CONVERSATION_with_USER', 'BOT_RESPONSE_CONVERSATION_next', 'new_data', 'context_length']

================================================================================
XỬ LÝ 5 DÒNG ĐẦU TIÊN
================================================================================

Đang xử lý dữ liệu...
...
✅ Đã lưu kết quả vào: result_sample_5_rows.xlsx
```

## Lưu ý

- File Excel đầu vào phải có 2 cột: `BOT_RESPONSE_CONVERSATION_with_USER` và `BOT_RESPONSE_CONVERSATION_next`
- Cột `BOT_RESPONSE_CONVERSATION_with_USER` phải chứa JSON string dạng list of dictionaries
- Script sẽ tự động tạo cột `new_data` mới

