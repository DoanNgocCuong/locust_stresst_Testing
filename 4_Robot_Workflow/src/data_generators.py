"""
Module sinh dữ liệu test cho Robot Workflow Locust test.
Tuân thủ nguyên tắc Single Responsibility:
- Chỉ chịu trách nhiệm tạo conversation_id và payloads.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Dict, Any, Optional, Sequence


def generate_conversation_id(
    prefix: str = "conv_doanngoccuong_locustTest"
) -> str:
    """
    Sinh conversation_id duy nhất dựa trên timestamp và random suffix.
    """
    timestamp = int(time.time() * 1000)
    random_suffix = random.randint(100, 999)
    return f"{prefix}_{timestamp}_{random_suffix}"


@dataclass
class InitConversationPayload:
    bot_id: int
    conversation_id: str
    input_slots: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bot_id": self.bot_id,
            "conversation_id": self.conversation_id,
            "input_slots": self.input_slots,
        }


@dataclass
class WebhookPayload:
    conversation_id: str
    message: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "conversation_id": self.conversation_id,
            "message": self.message,
        }


class MessageFactory:
    """Sinh user message ngẫu nhiên từ danh sách cho sẵn."""

    def __init__(self, messages: Sequence[str]):
        if not messages:
            raise ValueError("MessageFactory requires at least one message.")
        self._messages = list(messages)

    def random_message(self) -> str:
        return random.choice(self._messages)


class PayloadFactory:
    """Factory tạo payload cho các API."""

    def __init__(self, bot_id: int, messages: Sequence[str]):
        self.bot_id = bot_id
        self.message_factory = MessageFactory(messages)

    def build_init_payload(
        self,
        conversation_id: Optional[str] = None,
        input_slots: Optional[Dict[str, Any]] = None,
    ) -> InitConversationPayload:
        return InitConversationPayload(
            bot_id=self.bot_id,
            conversation_id=conversation_id or generate_conversation_id(),
            input_slots=input_slots or {},
        )

    def build_webhook_payload(
        self, conversation_id: str, message: Optional[str] = None
    ) -> WebhookPayload:
        return WebhookPayload(
            conversation_id=conversation_id,
            message=message or self.message_factory.random_message(),
        )


