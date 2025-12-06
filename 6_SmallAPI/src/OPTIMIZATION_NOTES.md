# 🚀 Tối ưu hóa Load Data

## ❌ Vấn đề ban đầu

### 1. Mỗi user load lại file Excel
- **Trước:** Mỗi user instance load lại file Excel 5949 dòng trong `on_start()`
- **Hậu quả:** 
  - Tốn thời gian và bộ nhớ
  - Load 100 users = load 100 lần file Excel
  - Log spam: "✅ Đã load 5949 dòng dữ liệu..." xuất hiện 100 lần

### 2. Thời gian load bị tính vào response time
- **Trước:** `on_start()` được gọi khi user bắt đầu, Locust có thể tính thời gian này
- **Hậu quả:** 
  - Response time không chính xác
  - Thời gian load Excel (vài giây) bị tính vào metrics

## ✅ Giải pháp

### 1. Shared Loader Pattern
- **Sau:** Load Excel data **1 lần duy nhất** khi module được import
- **Cơ chế:**
  - Load data ở module level (trước khi Locust chạy)
  - Tất cả users dùng chung 1 instance
  - Thread-safe với lock để đảm bảo chỉ load 1 lần

### 2. Load trước khi Locust chạy
- **Sau:** Load data khi import module (trước khi Locust bắt đầu)
- **Lợi ích:**
  - Không tính vào response time
  - Metrics chính xác hơn
  - Performance tốt hơn

## 📝 Code Changes

### `excel_data_loader.py`
```python
# Thêm shared loader với thread-safe
_shared_loader: Optional[ExcelDataLoader] = None
_loader_lock = threading.Lock()

def get_shared_loader(excel_path: Optional[str] = None) -> Optional[ExcelDataLoader]:
    """Lấy shared loader instance (load 1 lần duy nhất)"""
    global _shared_loader
    if _shared_loader is not None:
        return _shared_loader
    
    with _loader_lock:
        if _shared_loader is not None:
            return _shared_loader
        _shared_loader = ExcelDataLoader(excel_path)
        return _shared_loader
```

### `locustfile.py`
```python
# Load data khi import module (trước khi Locust chạy)
_shared_excel_loader = None
if Config.EXCEL_DATA_PATH:
    excel_file = Path(Config.EXCEL_DATA_PATH)
    if excel_file.exists():
        _shared_excel_loader = get_shared_loader(str(excel_file))

# on_start() chỉ sử dụng shared loader (không load lại)
def on_start(self):
    use_excel_data = _shared_excel_loader is not None
    self.payload_factory = ChatCompletionPayloadFactory(
        excel_loader=_shared_excel_loader,
        use_excel_data=use_excel_data
    )
```

## 📊 Kết quả

### Trước:
```
✅ Đã load 5949 dòng dữ liệu từ result_all_rows.xlsx
✅ User QwenAPIUser: Đã load dữ liệu từ Excel
✅ Đã load 5949 dòng dữ liệu từ result_all_rows.xlsx
✅ User QwenAPIUser: Đã load dữ liệu từ Excel
... (lặp lại 100 lần)
```

### Sau:
```
✅ [Module Init] Đã load 5949 dòng dữ liệu từ Excel (chia sẻ cho tất cả users)
[2025-12-06 12:46:37,189] Starting Locust 2.42.6
[2025-12-06 12:46:53,577] Ramping to 100 users...
```

## ✅ Lợi ích

1. **Performance:** Load 1 lần thay vì 100 lần
2. **Memory:** Tiết kiệm bộ nhớ (chỉ 1 instance)
3. **Accuracy:** Response time chính xác hơn (không tính thời gian load)
4. **Clean logs:** Không spam log khi khởi tạo users

