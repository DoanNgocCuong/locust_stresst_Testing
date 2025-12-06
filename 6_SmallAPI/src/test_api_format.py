"""
Script test để kiểm tra payload có đúng format API không.
So sánh với format trong README_API_Qwen3_1.7B.md
"""

import json
from pathlib import Path
from excel_data_loader import ExcelDataLoader
from data_generators import ChatCompletionPayloadFactory

# Đường dẫn file Excel
excel_path = Path(__file__).parent.parent / "data" / "result_all_rows.xlsx"

print("="*80)
print("KIỂM TRA FORMAT API")
print("="*80)

if excel_path.exists():
    try:
        # Load dữ liệu từ Excel
        loader = ExcelDataLoader(str(excel_path))
        factory = ChatCompletionPayloadFactory(
            excel_loader=loader,
            use_excel_data=True
        )
        
        # Tạo payload
        payload = factory.build_payload()
        payload_dict = payload.to_dict()
        
        print("\n📋 Payload JSON:")
        print(json.dumps(payload_dict, indent=2, ensure_ascii=False))
        
        print("\n" + "="*80)
        print("KIỂM TRA CÁC TRƯỜNG BẮT BUỘC:")
        print("="*80)
        
        # Kiểm tra các trường bắt buộc
        checks = {
            "model": "model" in payload_dict and payload_dict["model"] == "Qwen/Qwen3-1.7B",
            "messages": "messages" in payload_dict and isinstance(payload_dict["messages"], list),
            "temperature": "temperature" in payload_dict and payload_dict["temperature"] == 0.0,
            "repetition_penalty": "repetition_penalty" in payload_dict and payload_dict["repetition_penalty"] == 1.1,
            "stream": "stream" in payload_dict and payload_dict["stream"] == False,
            "chat_template_kwargs": "chat_template_kwargs" in payload_dict,
            "enable_thinking trong chat_template_kwargs": (
                "chat_template_kwargs" in payload_dict and 
                "enable_thinking" in payload_dict["chat_template_kwargs"] and
                payload_dict["chat_template_kwargs"]["enable_thinking"] == False
            ),
        }
        
        all_passed = True
        for check_name, check_result in checks.items():
            status = "✅" if check_result else "❌"
            print(f"{status} {check_name}: {check_result}")
            if not check_result:
                all_passed = False
        
        print("\n" + "="*80)
        print("KIỂM TRA FORMAT MESSAGE:")
        print("="*80)
        
        # Kiểm tra format message
        user_msg = next((m for m in payload_dict["messages"] if m["role"] == "user"), None)
        if user_msg:
            content = user_msg["content"]
            has_previous_question = "Previous Question:" in content
            has_previous_answer = "Previous Answer:" in content
            has_response_to_check = "Response to check:" in content
            
            print(f"✅ Có 'Previous Question:': {has_previous_question}")
            print(f"✅ Có 'Previous Answer:': {has_previous_answer}")
            print(f"✅ Có 'Response to check:': {has_response_to_check}")
            
            if has_previous_question and has_previous_answer and has_response_to_check:
                print("\n✅ Format message đúng!")
            else:
                print("\n❌ Format message chưa đúng!")
                all_passed = False
        
        print("\n" + "="*80)
        if all_passed:
            print("✅ TẤT CẢ KIỂM TRA ĐỀU PASS!")
        else:
            print("❌ CÓ LỖI TRONG FORMAT!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"\n❌ File không tồn tại: {excel_path}")

