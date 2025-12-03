"""
Script to run multiple simulations and export to Excel
"""

import os
import json
import dotenv
from openai import OpenAI
from def_ApiClientB import AICoachAPI
from def_simulate_with_api import simulate_with_api
from export_to_excel import export_to_excel, export_multiple_simulations_to_excel
from datetime import datetime


def run_single_simulation(bot_id, roleA_prompt, max_turns, initial_message="sẵn sàng", simulation_name=""):
    """
    Run a single simulation and return results.
    
    Args:
        bot_id: Bot ID to use
        roleA_prompt: Prompt for RoleA
        max_turns: Maximum number of turns
        initial_message: Initial message from RoleA
        simulation_name: Name for this simulation (for logging)
    
    Returns:
        dict: Results containing message_history, response_times, full_logs, and metadata
    """
    print(f"\n{'='*60}")
    print(f"🚀 Bắt đầu simulation: {simulation_name}")
    print(f"{'='*60}")
    
    # Lấy OpenAI API key từ biến môi trường
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in environment")
        return None
    
    # Khởi tạo OpenAI client
    openai_client = OpenAI(api_key=openai_api_key)
    
    # Khởi tạo API client
    api_client = AICoachAPI(bot_id=bot_id)
    
    if not api_client.init_conversation():
        print(f"❌ ERROR: Không thể khởi tạo cuộc trò chuyện với API")
        return None
    
    # Initial history
    initial_history = [{"role": "roleA", "content": initial_message}]
    
    # Chạy mô phỏng
    print(f"📝 Đang chạy simulation với {max_turns} lượt...")
    try:
        message_history, response_times, full_logs = simulate_with_api(
            roleA_prompt=roleA_prompt,
            maxTurns=max_turns,
            openai_client=openai_client,
            api_client=api_client,
            initialConversationHistory=json.dumps(initial_history)
        )
        
        return {
            "message_history": message_history,
            "response_times": response_times,
            "full_logs": full_logs,
            "api_client": api_client,
            "simulation_name": simulation_name,
            "bot_id": bot_id,
            "max_turns": max_turns
        }
    except Exception as e:
        print(f"❌ ERROR: Simulation failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None


def main():
    """Main function to run multiple simulations"""
    # Tải biến môi trường từ file .env
    dotenv.load_dotenv()
    
    print("="*60)
    print("🎯 CHƯƠNG TRÌNH CHẠY NHIỀU SIMULATION")
    print("="*60)
    
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
- Use "Tớ" (self) and "Cậu" (the other).
- NO icons. NO emoji.

STYLE RULES (VERY IMPORTANT):
- Speak like a REAL 6-year-old: natural emotions (oa, ồ, hay quá, hơ…), curiosity, may hesitate/mis-say then self-correct.
- React to what you "see/hear" from the robot (image/audio/object), not formulaic assistant talk.
- Be brief, natural, and stay on the current task.
- DO NOT proactively ask back (e.g., "Cậu muốn gì?", "Tiếp theo làm gì?", "Cần gì nữa không?").
- DO NOT offer help proactively (e.g., "Tớ sẵn sàng giúp", "Để tớ giúp Sam", "Tớ sẽ giúp cậu").
- Ask questions only when the robot EXPLICITLY asks you to or uses a direct "?" to you.
- Do not start new topics. Only respond to what the robot just presented.

QUALITY CHECK (BEFORE ANSWERING):
- [ ] 2–3 phrases, each 3–4 words
- [ ] Single line, separated by periods
- [ ] Natural childlike tone
- [ ] No asking back / no offering help
- [ ] Aligned with the robot's latest content
"""
    
    # Nhập số lượt
    max_turns = int(input("\n📊 Nhập số lượt tối đa cho mỗi simulation (ví dụ: 5): "))
    
    # Nhập số lượng simulation
    num_simulations = int(input("🔄 Nhập số lượng simulation muốn chạy (ví dụ: 2): "))
    
    # Nhập bot_id
    bot_id = int(input("🤖 Nhập Bot ID (ví dụ: 177): ") or "177")
    
    # Tạo thư mục results
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Chạy các simulation
    all_results = []
    for i in range(num_simulations):
        simulation_name = f"Simulation_{i+1}"
        print(f"\n{'='*60}")
        print(f"🔄 Đang chạy {simulation_name} ({i+1}/{num_simulations})...")
        print(f"{'='*60}")
        
        result = run_single_simulation(
            bot_id=bot_id,
            roleA_prompt=roleA_prompt,
            max_turns=max_turns,
            initial_message="sẵn sàng",
            simulation_name=simulation_name
        )
        
        if result:
            all_results.append(result)
            print(f"✅ {simulation_name} hoàn thành!")
        else:
            print(f"❌ {simulation_name} thất bại!")
    
    # Export kết quả ra Excel - TẤT CẢ VÀO 1 FILE VỚI NHIỀU SHEETS
    print(f"\n{'='*60}")
    print("📊 ĐANG XUẤT KẾT QUẢ RA FILE EXCEL")
    print(f"{'='*60}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"simulations_{timestamp}.xlsx"
    
    # Export tất cả simulation vào 1 file Excel với nhiều sheets
    excel_file = export_multiple_simulations_to_excel(
        simulation_results=all_results,
        output_dir=results_dir,
        filename=filename
    )
    
    # Tổng kết
    print(f"\n{'='*60}")
    print("🎉 HOÀN THÀNH TẤT CẢ SIMULATION")
    print(f"{'='*60}")
    print(f"✅ Đã chạy thành công: {len(all_results)}/{num_simulations} simulation")
    print(f"📁 Kết quả được lưu trong thư mục: {results_dir}")
    print(f"📊 File Excel duy nhất với 1 sheet chứa {len(all_results)} simulations: {excel_file}")
    
    # Hiển thị danh sách simulations
    if all_results:
        print("\n📋 Danh sách simulations trong file Excel:")
        for i, result in enumerate(all_results):
            simulation_name = result["simulation_name"]
            print(f"  {i+1}. {simulation_name}")


if __name__ == "__main__":
    main()

