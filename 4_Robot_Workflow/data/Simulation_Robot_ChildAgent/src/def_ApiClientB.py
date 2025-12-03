import time
import json
import requests
from openai import OpenAI
import os
from utils_convert_roles_for_api import convert_roles_for_api
import random


class AICoachAPI:
    """
    AICoachAPI class is used to send messages to a bot and receive responses from it.

    Attributes:
        base_url (str): The base URL of the API.
        timeout (int): The timeout for API requests in seconds.
        bot_id (int): The ID of the bot to interact with.
        current_conversation_id (str): The ID of the current conversation.

    Methods:
        init_conversation(): Initializes a new conversation with a unique conversation ID.
        send_message(message): Sends a message to the bot and returns the response.
    """
    def __init__(self, base_url="http://103.253.20.30:30000", timeout=30, bot_id=212):
        """Initializes the AICoachAPI with the base URL, timeout, and bot ID."""
        self.base_url = base_url
        # self.init_endpoint = f"{base_url}/personalized-ai-coach/api/v1/bot/initConversation"
        # self.webhook_endpoint = f"{base_url}/personalized-ai-coach/api/v1/bot/webhook"
        self.init_endpoint = f"{base_url}/robot-ai-workflow/api/v1/bot/initConversation"
        self.webhook_endpoint = f"{base_url}/robot-ai-workflow/api/v1/bot/webhook"
        self.current_conversation_id = None
        self.timeout = timeout
        self.bot_id = bot_id

    def init_conversation(self):
        """Initializes a new conversation and generates a unique conversation ID."""
        timestamp = int(time.time() * 1000)  # Convert to milliseconds
        random_suffix = str(random.randint(100, 999))
        conversation_id = f"conv_{timestamp}_{random_suffix}"
        
        # Sử dụng bot_id của đối tượng
        used_bot_id = self.bot_id
        
        payload = {
            "bot_id": used_bot_id,
            "conversation_id": conversation_id,
            "input_slots": {}
        }
        
        try:
            print(f"\n[AICoachAPI] Initializing conversation...")
            print(f"[AICoachAPI] Endpoint: {self.init_endpoint}")
            print(f"[AICoachAPI] Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                self.init_endpoint,
                headers={'Content-Type': 'application/json'},
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            print(f"[AICoachAPI] Init successful. Response: {json.dumps(response.json(), indent=2)}")
            self.current_conversation_id = conversation_id
            return True
            
        except requests.Timeout:
            print("[AICoachAPI] Error: Request timed out during initialization")
            return False
        except requests.RequestException as e:
            print(f"[AICoachAPI] Error during initialization: {str(e)}")
            return False

    def send_message(self, message):
        """
        Sends a message to the bot and returns the response with measured response time.
        
        Returns:
            dict: Response data with 'response' and 'response_time' keys, or None if error
            Format: {"response": {...}, "response_time": 0.123456}
        """
        if not self.current_conversation_id:
            print("[AICoachAPI] Error: No active conversation. Initializing new one...")
            if not self.init_conversation():
                return None

        payload = {
            "conversation_id": self.current_conversation_id,
            "message": message
        }
        
        try:
            print(f"\n[AICoachAPI] Sending message...")
            print(f"[AICoachAPI] Endpoint: {self.webhook_endpoint}")
            print(f"[AICoachAPI] Payload: {json.dumps(payload, indent=2)}")
            
            # Measure response time
            start_time = time.time()
            response = requests.post(
                self.webhook_endpoint,
                headers={'Content-Type': 'application/json'},
                json=payload,
                timeout=self.timeout
            )
            end_time = time.time()
            response_time = round(end_time - start_time, 6)
            
            response.raise_for_status()
            # Trả ra response_data
            response_data = response.json()
            
            # Add measured response time to response data
            response_data["measured_response_time"] = response_time
            
            print(f"[AICoachAPI] Message sent successfully. Response time: {response_time:.6f}s")
            print(f"[AICoachAPI] Response: {json.dumps(response_data, indent=2)}")
            
            return {
                "response": response_data,
                "response_time": response_time
            }
            
        except requests.Timeout:
            end_time = time.time()
            response_time = round(end_time - start_time, 6) if 'start_time' in locals() else 0
            print(f"[AICoachAPI] Error: Request timed out while sending message (elapsed: {response_time:.6f}s)")
            # Return error result with response_time for tracking
            return {
                "response": None,
                "response_time": response_time,
                "error": "timeout"
            }
        except requests.RequestException as e:
            end_time = time.time()
            response_time = round(end_time - start_time, 6) if 'start_time' in locals() else 0
            print(f"[AICoachAPI] Error sending message: {str(e)} (elapsed: {response_time:.6f}s)")
            # Return error result with response_time for tracking
            return {
                "response": None,
                "response_time": response_time,
                "error": str(e)
            }
