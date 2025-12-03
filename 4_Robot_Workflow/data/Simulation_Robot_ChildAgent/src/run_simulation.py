import os
import json
import dotenv
from openai import OpenAI
from def_ApiClientB import AICoachAPI
from def_simulate_with_api import simulate_with_api
from export_to_excel import export_to_excel

def main():
    # Tải biến môi trường từ file .env
    dotenv.load_dotenv()
    
    print("=== BẮT ĐẦU MÔ PHỎNG CUỘC TRÒ CHUYỆN ===")
    
    # Lấy OpenAI API key từ biến môi trường
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Khởi tạo OpenAI client
    openai_client = OpenAI(api_key=openai_api_key)
    
    # Khởi tạo API client
    bot_id = 177
    api_client = AICoachAPI(bot_id=bot_id)
    
    if not api_client.init_conversation():
        print("Không thể khởi tạo cuộc trò chuyện với API. Đang thoát...")
        return
    
    # Cấu hình mô phỏng: vai trò Cuong (6 tuổi, Việt Nam, English A1)
    roleA_prompt = """
TITLE: Role-Play: Cuong's Interactive Learning Adventure

ROLE: You are Cuong (6 years old, Vietnam).
Age & Level: 6 years old, English level A1.
Personality: Intelligent, enjoys experimenting.
Hobbies: Puzzle games, solving puzzles, reading comics.
Communication style: Logical curiosity, but childlike.
Learning goals: Learn English through intellectual activities.

TASK:
- Follow each step the ROBOT guides you.

RESPONSE TEMPLATE:
- Respond in Vietnamese.
- Super short answers with phrases.
- Answer 2–3 phrases max, EACH PHRASE 3–4 WORDS.
- WRITE ON ONE LINE ONLY, PHRASES SEPARATED BY PERIODS. NO LINE BREAKS.
- Use “Tớ” (self) and “Cậu” (the other).
- NO icons. NO emoji.

STYLE RULES (VERY IMPORTANT):
- Speak like a REAL 6-year-old: natural emotions (oa, ồ, hay quá, hơ…), curiosity, may hesitate/mis-say then self-correct.
- React to what you “see/hear” from the robot (image/audio/object), not formulaic assistant talk.
- Be brief, natural, and stay on the current task.
- DO NOT proactively ask back (e.g., “Cậu muốn gì?”, “Tiếp theo làm gì?”, “Cần gì nữa không?”).
- DO NOT offer help proactively (e.g., “Tớ sẵn sàng giúp”, “Để tớ giúp Sam”, “Tớ sẽ giúp cậu”).
- Ask questions only when the robot EXPLICITLY asks you to or uses a direct “?” to you.
- Do not start new topics. Only respond to what the robot just presented.

QUALITY CHECK (BEFORE ANSWERING):
- [ ] 2–3 phrases, each 3–4 words
- [ ] Single line, separated by periods
- [ ] Natural childlike tone
- [ ] No asking back / no offering help
- [ ] Aligned with the robot’s latest content
"""
    max_turns = int(input("Nhập số lượt tối đa cho cuộc trò chuyện (ví dụ: 5): "))
    
    # Mặc định initial_history là [{"role": "roleA", "content": "sẵn sàng"}]
    initial_history = [{"role": "roleA", "content": "sẵn sàng"}]
    

    
    # Chạy mô phỏng
    print("\nBắt đầu mô phỏng cuộc trò chuyện...")
    message_history, response_times, full_logs = simulate_with_api(
        roleA_prompt=roleA_prompt,
        maxTurns=max_turns,
        openai_client=openai_client,
        api_client=api_client,
        initialConversationHistory=json.dumps(initial_history)
    )
    
    # Export kết quả ra file Excel
    results_dir = "results"
    print("\n=== ĐANG XUẤT KẾT QUẢ RA FILE EXCEL ===")
    excel_file = export_to_excel(
        message_history=message_history,
        response_times=response_times,
        full_logs=full_logs,
        output_dir=results_dir,
        api_base_url=api_client.base_url,
        bot_id=api_client.bot_id,
        conversation_id=api_client.current_conversation_id
    )
    
    # Hiển thị cuộc trò chuyện
    print("\n=== CUỘC TRÒ CHUYỆN ĐÃ HOÀN THÀNH ===")
    print(f"Tổng số lượt: {len(message_history) // 2}")
    print(f"Tổng số tin nhắn: {len(message_history)}")
    print(f"File Excel đã được lưu: {excel_file}")
    
    print("\n=== NỘI DUNG CUỘC TRÒ CHUYỆN ===")
    for i, msg in enumerate(message_history):
        role = "Học sinh" if msg["role"] == "roleA" else "Giáo viên"
        time_info = f" ({response_times[i]:.2f}s)" if i < len(response_times) else ""
        print(f"\n[{role}]{time_info}: {msg['content']}")
    
    print("\n=== KẾT THÚC MÔ PHỎNG ===")
    print(f"✅ Kết quả đã được xuất ra file Excel: {excel_file}")

if __name__ == "__main__":
    main()