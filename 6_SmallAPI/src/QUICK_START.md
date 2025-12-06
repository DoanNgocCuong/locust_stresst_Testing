# 🚀 Quick Start - Stress Test với Excel Data

## Bước 1: Cài đặt dependencies

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\src
pip install -r requirements.txt
```

## Bước 2: Đảm bảo có file Excel

File mặc định: `6_SmallAPI/data/result_all_rows.xlsx`

Nếu chưa có, chạy:

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\data
python generate_new_data.py --all
```

## Bước 3: Chạy Stress Test

### Chạy với Web UI (khuyến nghị cho lần đầu)

```powershell
cd D:\GIT\locust_stresst_Testing\6_SmallAPI\src
.\run_test.ps1
```

Mở browser: http://localhost:8089

### Chạy Headless (tự động)

```powershell
.\run_test.ps1 10 2 60s headless
```

Tham số:
- `10`: Số users
- `2`: Spawn rate (users/second)
- `60s`: Thời gian chạy
- `headless`: Chạy không có UI

## ✅ Kiểm tra

Script sẽ tự động:
- ✅ Load dữ liệu từ Excel (5949 dòng)
- ✅ Sử dụng dữ liệu từ cột `new_data` làm content cho role `user`
- ✅ Format: `Previous Question: ...\nPrevious Answer: ...\nResponse to check: ...`

## 📊 Kết quả

Sau khi chạy headless, kết quả sẽ ở:
- HTML: `6_SmallAPI/results/report_*.html`
- CSV: `6_SmallAPI/results/results_*.csv`

## 🔧 Test thủ công

```powershell
# Test Excel loader
python test_excel_loader.py

# Test Payload factory
python test_payload_factory.py
```

