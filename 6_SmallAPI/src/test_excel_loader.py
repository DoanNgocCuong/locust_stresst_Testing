"""
Script test để kiểm tra ExcelDataLoader hoạt động đúng không.
"""

from pathlib import Path
from excel_data_loader import ExcelDataLoader

# Đường dẫn file Excel
excel_path = Path(__file__).parent.parent / "data" / "result_all_rows.xlsx"

print(f"Đang kiểm tra file: {excel_path}")
print(f"File tồn tại: {excel_path.exists()}")

if excel_path.exists():
    try:
        loader = ExcelDataLoader(str(excel_path))
        print(f"\n✅ Đã load thành công!")
        print(f"   - Số lượng dòng dữ liệu: {loader.get_data_count()}")
        
        # Lấy 3 mẫu ngẫu nhiên
        print(f"\n📋 3 mẫu dữ liệu ngẫu nhiên:")
        for i in range(3):
            data = loader.get_random_new_data()
            print(f"\n--- Mẫu {i+1} ---")
            print(data[:200] + "..." if len(data) > 200 else data)
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"\n❌ File không tồn tại!")
    print(f"   Hãy chạy: cd 6_SmallAPI/data && python generate_new_data.py --all")

