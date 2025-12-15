# Các lệnh chạy script generate_new_data.py

## 📦 Cài đặt dependencies

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\data
pip install -r requirements.txt
```

## 🚀 Các lệnh chạy

### 1. Chạy 5 dòng đầu (mặc định)

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\data
python generate_new_data.py
```

Hoặc:

```powershell
python generate_new_data.py --sample 5
```

**Kết quả:** `result_sample_5_rows.xlsx`

---

### 2. Chạy hàng loạt (toàn bộ file - 5949 dòng)

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\data
python generate_new_data.py --all
```

**Kết quả:** `result_all_rows.xlsx`

---

### 3. Chạy số dòng tùy chỉnh

```powershell
# Chạy 10 dòng đầu
python generate_new_data.py --sample 10

# Chạy 100 dòng đầu
python generate_new_data.py --sample 100
```

---

### 4. Chỉ định file đầu vào/đầu ra

```powershell
# Chỉ định file đầu vào
python generate_new_data.py --sample 5 --input "custom_input.xlsx"

# Chỉ định file đầu ra
python generate_new_data.py --all --output "custom_output.xlsx"

# Cả hai
python generate_new_data.py --sample 10 --input "input.xlsx" --output "output.xlsx"
```

---

## 📋 Xem help

```powershell
python generate_new_data.py --help
```

---

## ⚠️ Lưu ý

- Nếu file output đang được mở trong Excel, script sẽ tự động tạo file mới với timestamp
- File Excel đầu vào phải có 2 cột: `BOT_RESPONSE_CONVERSATION_with_USER` và `BOT_RESPONSE_CONVERSATION_next`
- Script sẽ tự động tạo cột `new_data` mới

---

## 📊 Ví dụ output

```
Đang đọc file: D:\GIT\locust_stresst_Testing\6_SmallAPI\data\data_for_stressTest.xlsx

Tổng số dòng trong file: 5949
Các cột trong file: ['conversationID', 'BOT_RESPONSE_CONVERSATION_with_USER', ...]

================================================================================
XỬ LÝ 5 DÒNG ĐẦU TIÊN
================================================================================

Đang xử lý dữ liệu...
...
✅ Đã lưu kết quả vào: result_sample_5_rows.xlsx
   - Tổng số dòng đã xử lý: 5
```







