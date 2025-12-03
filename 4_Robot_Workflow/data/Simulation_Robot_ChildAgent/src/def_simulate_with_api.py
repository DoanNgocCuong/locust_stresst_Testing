import json
import time
from def_promptA import generate_roleA_response

def extract_text_from_api_response(api_response):
    """
    Extract and combine all text from API response.
    
    Args:
        api_response: API response dict with 'text' field
        
    Returns:
        str: Combined text from all text items, separated by spaces
    """
    if not api_response or "text" not in api_response:
        return ""
    
    text_list = api_response.get("text", [])
    if not isinstance(text_list, list) or len(text_list) == 0:
        return ""
    
    # Extract text from each item
    extracted_texts = []
    for item in text_list:
        if isinstance(item, dict):
            # New format: object with 'text' property
            text = item.get("text", "")
            if text:
                extracted_texts.append(text)
        elif isinstance(item, str):
            # Old format: string
            extracted_texts.append(item)
    
    # Join all texts with space
    return " ".join(extracted_texts).strip()

def simulate_with_api(roleA_prompt, maxTurns, openai_client, api_client, initialConversationHistory=None):
    """Simulate conversation using OpenAI for RoleA and API for RoleB"""
    message_history = []
    response_times = []
    full_log = []  # Lưu toàn bộ response từ API
    conversationTurnCount = 0

    print("\n=== Initial Settings ===")
    print(f"RoleA Prompt: {roleA_prompt[:100]}..." if roleA_prompt else "RoleA Prompt: None")
    print(f"Max Turns: {maxTurns}")

    # Get initial message from history
    initial_message = "sẵn sàng"  # default
    if initialConversationHistory is not None:
        try:
            history = json.loads(initialConversationHistory)
            if history and history[0]["role"] == "roleA":
                initial_message = history[0]["content"]
                # Add initial roleA message to history
                message_history.append({"role": "roleA", "content": initial_message})
                full_log.append("")  # Empty log for roleA message
                response_times.append(0)  # 0 for initial message
            print(f"\nUsing initial message: {initial_message}")
        except json.JSONDecodeError as e:
            print(f"Error parsing conversation history: {e}")

    # Start with RoleB using the initial message
    print(f"\n=== Starting with RoleB (initial message: {initial_message}) ===")
    api_result = api_client.send_message(initial_message)
    
    if api_result and api_result.get("response"):
        api_response = api_result["response"]
        response_time = api_result.get("response_time", 0)
        
        # Extract all text from API response
        roleB_message = extract_text_from_api_response(api_response)
            
        print(f"RoleB response: {roleB_message[:100]}...")
        print(f"RoleB response time: {response_time:.6f}s")
        message_history.append({"role": "roleB", "content": roleB_message})
        # Lưu toàn bộ response
        full_log.append(json.dumps(api_response, ensure_ascii=False, indent=2))
        response_times.append(response_time)
        
        if api_response.get("status") == "END":
            print("[INFO] Received END status from API. Ending conversation.")
            return message_history, response_times, full_log
    else:
        # Handle error case - still record response time if available
        response_time = api_result.get("response_time", 0) if api_result else 0
        print(f"[ERROR] Failed to get initial response from API (elapsed: {response_time:.6f}s)")
        response_times.append(response_time)
        full_log.append("")  # Empty log for error
        return message_history, response_times, full_log

    # Start conversation loop
    print(f"\n=== Starting conversation loop (max turns: {maxTurns}) ===")
    while conversationTurnCount < maxTurns:
        try:
            print(f"\n--- Turn {conversationTurnCount + 1}/{maxTurns} ---")
            
            # RoleA turn with OpenAI (with fallback)
            print("Generating RoleA response with OpenAI...")
            try:
                roleA_message, roleA_time = generate_roleA_response(
                    openai_client,
                    roleA_prompt,
                    message_history
                )
            except Exception as openai_error:
                print(f"OpenAI Error: {openai_error}")
                print("Using fallback response for RoleA...")
                # Fallback response when OpenAI fails
                roleA_message = f"Tôi muốn biết thêm về chủ đề này. Bạn có thể giải thích chi tiết hơn không?"
                roleA_time = 0.1
                
            print(f"RoleA response: {roleA_message[:100]}...")
            message_history.append({"role": "roleA", "content": roleA_message})
            full_log.append("")  # Empty log for roleA message
            response_times.append(round(roleA_time, 6))

            # RoleB turn with API
            print("Sending message to RoleB API...")
            api_result = api_client.send_message(roleA_message)

            if api_result and api_result.get("response"):
                api_response = api_result["response"]
                response_time = api_result.get("response_time", 0)
                
                # Extract all text from API response
                roleB_message = extract_text_from_api_response(api_response)
                    
                print(f"RoleB response: {roleB_message[:100]}...")
                print(f"RoleB response time: {response_time:.6f}s")
                message_history.append({"role": "roleB", "content": roleB_message})
                # Lưu toàn bộ response
                full_log.append(json.dumps(api_response, ensure_ascii=False, indent=2))
                response_times.append(response_time)
                
                if api_response.get("status") == "END":
                    print("[INFO] Received END status from API. Ending conversation.")
                    break
            else:
                # Handle error case - still record response time if available
                response_time = api_result.get("response_time", 0) if api_result else 0
                print(f"[ERROR] Failed to get response from API (elapsed: {response_time:.6f}s)")
                full_log.append("")  # Empty log for failed API response
                response_times.append(response_time)  # Record actual elapsed time even on error
                break

            conversationTurnCount += 1
            print(f"\n=== End of Turn {conversationTurnCount}/{maxTurns} ===")
            time.sleep(1)

        except Exception as e:
            print(f"\nError during conversation: {str(e)}")
            print(f"Exception type: {type(e).__name__}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            full_log.append("")  # Empty log for error case
            break

    print(f"\n=== Conversation ended. Total turns: {conversationTurnCount}/{maxTurns} ===")
    return message_history, response_times, full_log
