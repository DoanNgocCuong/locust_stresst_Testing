Đang kiểm tra cấu trúc code hiện tại để tích hợp stress test dùng role user với dữ liệu từ cột `new_data`:

[4 tools called]

Đang tạo module đọc dữ liệu từ Excel và cập nhật code để dùng dữ liệu từ cột `new_data`:

[9 tools called]

Đang kiểm tra lỗi và tạo file hướng dẫn chạy:

[2 tools called]

Đang tạo file hướng dẫn và kiểm tra file Excel:

[3 tools called]

File Excel đã có. Đang tạo script test để kiểm tra:

[2 tools called]

Đang kiểm tra payload factory với dữ liệu từ Excel:

[2 tools called]

Tạo file hướng dẫn chạy nhanh:

[2 tools called]

## Hoàn thành

### Files đã tạo/cập nhật

1. `6_SmallAPI/src/excel_data_loader.py` — Module đọc dữ liệu từ Excel

   - Class `ExcelDataLoader` để load và quản lý dữ liệu từ file Excel
   - Hỗ trợ lấy dữ liệu ngẫu nhiên từ cột `new_data`
2. `6_SmallAPI/src/data_generators.py` — Cập nhật

   - Thêm hỗ trợ `ExcelDataLoader` trong `ChatCompletionPayloadFactory`
   - Tham số `excel_loader` và `use_excel_data`
   - Method `build_payload()` sử dụng dữ liệu từ Excel nếu có
3. `6_SmallAPI/src/locustfile.py` — Cập nhật

   - Tự động load dữ liệu từ Excel trong `on_start()`
   - Fallback về dữ liệu mẫu nếu không tìm thấy Excel
4. `6_SmallAPI/src/config.py` — Cập nhật

   - Thêm `EXCEL_DATA_PATH` để cấu hình đường dẫn file Excel
5. `6_SmallAPI/src/requirements.txt` — Cập nhật

   - Thêm `pandas>=2.0.0` và `openpyxl>=3.1.0`
6. `6_SmallAPI/src/README_STRESS_TEST.md` — Hướng dẫn chi tiết
7. `6_SmallAPI/src/QUICK_START.md` — Hướng dẫn nhanh
8. `6_SmallAPI/src/test_excel_loader.py` — Script test Excel loader
9. `6_SmallAPI/src/test_payload_factory.py` — Script test Payload factory

### Cách hoạt động

1. Load dữ liệu: Script tự động load file `result_all_rows.xlsx` (5949 dòng)
2. Format message: Sử dụng dữ liệu từ cột `new_data` làm `content` cho role `user`:
   ```json
   {
       "role": "user",
       "content": "Previous Question: Tớ buồn quá.\nPrevious Answer: i think a yummy\nResponse to check: Nghe vui quá! Bể Hả, cậu có muốn chơi trò kể tên các loại trái cây bằng tiếng Anh không? Name fruits in English!"
   }
   ```
3. Random selection: Mỗi request chọn ngẫu nhiên một dòng từ 5949 dòng dữ liệu

### Lệnh chạy

```powershell
# 1. Cài đặt dependencies
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\src
pip install -r requirements.txt

# 2. Chạy stress test với Web UI
.\run_test.ps1

# 3. Hoặc chạy headless
.\run_test.ps1 10 2 60s headless
```

### Test đã chạy

- Excel loader: Đã load 5949 dòng dữ liệu
- Payload factory: Tạo payload đúng format với dữ liệu từ Excel
- Format validation: Tất cả payload đều có đủ "Previous Question", "Previous Answer", "Response to check"

### Tính năng

- Tự động load Excel: Script tự động tìm và load file Excel
- Fallback: Nếu không tìm thấy Excel, dùng dữ liệu mẫu
- Random data: Mỗi request dùng dữ liệu ngẫu nhiên từ Excel
- Tuân thủ SOLID: Code rõ ràng, dễ bảo trì

Bạn có thể chạy stress test với dữ liệu từ Excel.
