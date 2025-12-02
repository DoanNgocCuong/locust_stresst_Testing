"""
Data generators module cho Locust test.
Chịu trách nhiệm tạo dữ liệu test động theo nguyên tắc Single Responsibility.
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from config import Config


class ConversationLogGenerator:
    """Class chịu trách nhiệm generate conversation logs."""
    
    # Sample conversation messages
    BOT_MESSAGES = [
        "<happy/> Chào cậu. <playful/> Hôm nay cậu thấy thế nào? <curious/> Có gì vui nhất đã xảy ra với cậu không?",
        "<sad/> Ồ, cậu muốn đi ngủ rồi sao? <playful/> Pika đoán cậu đã có một ngày thật vui nên giờ mới mệt đúng không?",
        "<worry/> Pika hiểu rồi. <sad/> Pika rất tiếc nhưng Pika không thể giúp cậu đi ngủ được.",
        "<surprised/> Ơ, Pika cứ tưởng cậu muốn đi ngủ chứ. <happy/> Vậy thì mình cùng học bài thôi!",
        "<happy/> Pika có nhiều chủ đề lắm! <playful/> Từ các con vật đáng yêu đến những món ăn ngon lành.",
        "<playful/> Pika không hiểu lắm. <curious/> Cậu có thể nói rõ hơn không?",
        "<happy/> Không có gì! <playful/> Vậy cậu đã sẵn sàng cho một nhiệm vụ mới từ hành tinh Popa chưa?",
        "<curious/> Cậu đang muốn Pika nhìn vào cái cốc nào vậy?",
        "<worry/> Pika không có mắt như cậu nên không thể tự nhìn thấy cái cốc được.",
    ]
    
    USER_MESSAGES = [
        "Tôi muốn đi ngủ.",
        "Rõ ràng tôi muốn học bài.",
        "Ơ, thế cậu có chủ đề gì?",
        "Được rồi, cảm ơn.",
        "Look at the cup.",
        "cốc nào á, tự biết chứ.",
        "kết thúc",
        "end conversation",
    ]
    
    @staticmethod
    def generate_conversation_logs(min_turns: int = 3, max_turns: int = 10) -> List[Dict[str, str]]:
        """
        Generate danh sách conversation logs ngẫu nhiên.
        
        Args:
            min_turns: Số lượt hội thoại tối thiểu
            max_turns: Số lượt hội thoại tối đa
            
        Returns:
            List các dictionary chứa conversation logs
        """
        logs = []
        num_turns = random.randint(min_turns, max_turns)
        
        for i in range(num_turns):
            # Bot response
            bot_content = random.choice(ConversationLogGenerator.BOT_MESSAGES)
            logs.append({
                "content": bot_content,
                "character": "BOT_RESPONSE_CONVERSATION"
            })
            
            # User message (trừ lượt cuối có thể để trống)
            if i < num_turns - 1:
                user_content = random.choice(ConversationLogGenerator.USER_MESSAGES)
                logs.append({
                    "content": user_content,
                    "character": "USER"
                })
            else:
                # Lượt cuối có thể có empty bot response
                logs.append({
                    "content": "",
                    "character": "BOT_RESPONSE_CONVERSATION"
                })
        
        return logs


class ConversationDataGenerator:
    """Class chịu trách nhiệm generate dữ liệu cho conversation end API."""
    
    @staticmethod
    def generate_conversation_id() -> str:
        """Generate conversation ID ngẫu nhiên."""
        return f"conv_{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def generate_user_id(prefix: str = "user_") -> str:
        """Generate user ID ngẫu nhiên."""
        return f"{prefix}{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def generate_timestamps() -> tuple[str, str]:
        """
        Generate start_time và end_time.
        
        Returns:
            Tuple (start_time, end_time) dạng ISO format
        """
        end_time = datetime.utcnow()
        duration_minutes = random.randint(5, 30)
        start_time = end_time - timedelta(minutes=duration_minutes)
        
        return (
            start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        )
    
    @staticmethod
    def generate_conversation_end_payload(
        conversation_id: str = None,
        user_id: str = None,
        bot_id: str = None,
        bot_name: str = None,
        bot_type: str = None,
        conversation_logs: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Generate payload hoàn chỉnh cho API conversation end.
        
        Args:
            conversation_id: ID của conversation (nếu None sẽ generate)
            user_id: ID của user (nếu None sẽ generate)
            bot_id: ID của bot
            bot_name: Tên bot
            bot_type: Loại bot
            conversation_logs: Danh sách logs (nếu None sẽ generate)
            
        Returns:
            Dictionary chứa payload cho API
        """
        start_time, end_time = ConversationDataGenerator.generate_timestamps()
        
        return {
            "conversation_id": conversation_id or ConversationDataGenerator.generate_conversation_id(),
            "user_id": user_id or ConversationDataGenerator.generate_user_id(),
            "bot_id": bot_id or Config.DEFAULT_BOT_ID,
            "bot_name": bot_name or Config.DEFAULT_BOT_NAME,
            "bot_type": bot_type or Config.DEFAULT_BOT_TYPE,
            "conversation_logs": conversation_logs or ConversationLogGenerator.generate_conversation_logs(),
            "end_time": end_time,
            "start_time": start_time,
            "status": "PENDING"
        }


class ActivitySuggestDataGenerator:
    """Class chịu trách nhiệm generate dữ liệu cho activity suggest API."""
    
    @staticmethod
    def generate_user_id(prefix: str = "user_") -> str:
        """Generate user ID ngẫu nhiên."""
        return f"{prefix}{uuid.uuid4().hex[:8]}"
    
    @staticmethod
    def generate_activity_suggest_payload(user_id: str = None) -> Dict[str, str]:
        """
        Generate payload cho API activity suggest.
        
        Args:
            user_id: ID của user (nếu None sẽ generate)
            
        Returns:
            Dictionary chứa payload cho API
        """
        return {
            "user_id": user_id or ActivitySuggestDataGenerator.generate_user_id()
        }

