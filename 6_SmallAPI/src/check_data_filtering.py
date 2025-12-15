"""
Kiểm tra số lượng dữ liệu hợp lệ sau khi lọc theo max_tokens.
"""

from pathlib import Path
from excel_data_loader import ExcelDataLoader
from config import Config

excel_path = Path(Config.EXCEL_DATA_PATH)
loader = ExcelDataLoader(str(excel_path))

print("="*80)
print("KIỂM TRA LỌC DỮ LIỆU THEO CONTEXT LENGTH")
print("="*80)

total_data = loader.get_data_count()
print(f"\nTổng số dòng dữ liệu: {total_data}")

# Kiểm tra với max_tokens = 200 (giới hạn an toàn)
max_tokens = 200
max_chars = max_tokens * 4  # ~4 ký tự = 1 token

valid_data = [
    data for data in loader.get_all_data()
    if len(data) <= max_chars
]

invalid_data = [
    data for data in loader.get_all_data()
    if len(data) > max_chars
]

print(f"\nGiới hạn: {max_tokens} tokens (~{max_chars} ký tự)")
print(f"✅ Dữ liệu hợp lệ: {len(valid_data)} dòng ({len(valid_data)/total_data*100:.1f}%)")
print(f"❌ Dữ liệu quá dài: {len(invalid_data)} dòng ({len(invalid_data)/total_data*100:.1f}%)")

if invalid_data:
    print(f"\nVí dụ dữ liệu quá dài (3 mẫu đầu):")
    for i, data in enumerate(invalid_data[:3], 1):
        print(f"\n--- Mẫu {i} ({len(data)} ký tự, ~{len(data)//4} tokens) ---")
        print(data[:200] + "...")

print(f"\n{'='*80}")
print("KẾT LUẬN:")
print(f"{'='*80}")
if len(valid_data) > 0:
    print(f"✅ Có {len(valid_data)} dòng dữ liệu hợp lệ để test")
    print(f"✅ Logic lọc đã hoạt động - chỉ lấy dữ liệu hợp lệ")
else:
    print(f"⚠️  Không có dữ liệu hợp lệ nào!")
    print(f"   Cần điều chỉnh max_tokens hoặc truncate dữ liệu")







