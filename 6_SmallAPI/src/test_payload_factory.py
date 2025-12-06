"""
Script test để kiểm tra ChatCompletionPayloadFactory với dữ liệu từ Excel.
"""

import json
from pathlib import Path
from excel_data_loader import ExcelDataLoader
from data_generators import ChatCompletionPayloadFactory

# Đường dẫn file Excel
excel_path = Path(__file__).parent.parent / "data" / "result_all_rows.xlsx"

print("="*80)
print("TEST PAYLOAD FACTORY VỚI DỮ LIỆU TỪ EXCEL")
print("="*80)

if excel_path.exists():
    try:
        # Load dữ liệu từ Excel
        loader = ExcelDataLoader(str(excel_path))
        print(f"\n✅ Đã load {loader.get_data_count()} dòng dữ liệu")
        
        # Tạo payload factory với Excel loader
        factory = ChatCompletionPayloadFactory(
            excel_loader=loader,
            use_excel_data=True
        )
        
        # Tạo 3 payload mẫu
        print(f"\n📋 Tạo 3 payload mẫu:")
        for i in range(3):
            payload = factory.build_payload()
            payload_dict = payload.to_dict()
            
            print(f"\n--- Payload {i+1} ---")
            print(f"Model: {payload_dict['model']}")
            print(f"Messages:")
            for msg in payload_dict['messages']:
                print(f"  - Role: {msg['role']}")
                if msg['role'] == 'user':
                    content_preview = msg['content'][:150] + "..." if len(msg['content']) > 150 else msg['content']
                    print(f"    Content: {content_preview}")
                else:
                    print(f"    Content: {msg['content'][:50]}...")
            
            # Kiểm tra format
            user_msg = next((m for m in payload_dict['messages'] if m['role'] == 'user'), None)
            if user_msg:
                content = user_msg['content']
                if 'Previous Question:' in content and 'Previous Answer:' in content and 'Response to check:' in content:
                    print(f"  ✅ Format đúng: Có Previous Question, Previous Answer, Response to check")
                else:
                    print(f"  ⚠️  Format không đúng")
        
        print(f"\n✅ Test thành công!")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"\n❌ File không tồn tại: {excel_path}")
    print(f"   Hãy chạy: cd 6_SmallAPI/data && python generate_new_data.py --all")

