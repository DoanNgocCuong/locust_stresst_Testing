"""
Test để xác nhận mỗi lần gọi API sẽ lấy data ngẫu nhiên khác nhau.
"""

from pathlib import Path
from excel_data_loader import get_shared_loader
from data_generators import ChatCompletionPayloadFactory
from config import Config

# Load shared loader
excel_path = Path(Config.EXCEL_DATA_PATH)
loader = get_shared_loader(str(excel_path))

if loader:
    factory = ChatCompletionPayloadFactory(
        excel_loader=loader,
        use_excel_data=True
    )
    
    print("="*80)
    print("KIỂM TRA: Mỗi API call có lấy data khác nhau không?")
    print("="*80)
    print(f"\nTổng số dòng dữ liệu: {loader.get_data_count()}")
    print(f"\nTạo 10 payload để kiểm tra:\n")
    
    # Tạo 10 payload và so sánh
    payloads = []
    for i in range(10):
        payload = factory.build_payload()
        user_content = payload.messages[1]["content"]  # Lấy content của user message
        payloads.append(user_content)
        print(f"Payload {i+1}: {user_content[:100]}...")
    
    print("\n" + "="*80)
    print("PHÂN TÍCH:")
    print("="*80)
    
    # Kiểm tra xem có trùng lặp không
    unique_payloads = set(payloads)
    duplicates = len(payloads) - len(unique_payloads)
    
    print(f"✅ Tổng số payload tạo: {len(payloads)}")
    print(f"✅ Số payload unique: {len(unique_payloads)}")
    print(f"✅ Số payload trùng lặp: {duplicates}")
    
    if duplicates == 0:
        print("\n✅ KẾT LUẬN: Mỗi API call lấy data KHÁC NHAU (random)")
    else:
        print(f"\n⚠️  KẾT LUẬN: Có {duplicates} payload trùng lặp (có thể do random trùng)")
        print("   (Với 5949 dòng dữ liệu, xác suất trùng trong 10 lần là rất thấp)")
    
    # So sánh chi tiết 2 payload đầu tiên
    print("\n" + "="*80)
    print("SO SÁNH 2 PAYLOAD ĐẦU TIÊN:")
    print("="*80)
    print(f"\nPayload 1:\n{payloads[0][:200]}...")
    print(f"\nPayload 2:\n{payloads[1][:200]}...")
    
    if payloads[0] != payloads[1]:
        print("\n✅ Payload 1 và Payload 2 KHÁC NHAU")
    else:
        print("\n⚠️  Payload 1 và Payload 2 GIỐNG NHAU (rất hiếm với random)")

