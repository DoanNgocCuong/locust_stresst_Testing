"""
Locust test cho Robot Workflow:
- API initConversation
- API webhook

Mỗi user sẽ giữ conversation_id riêng và gửi messages ngẫu nhiên.
"""

import json
from locust import HttpUser, task, between

from config import Config
from data_generators import PayloadFactory


class RobotWorkflowUser(HttpUser):
    """
    Mỗi Locust user tương ứng với 1 học viên mô phỏng.
    User sẽ:
      1. Khởi tạo conversation mới (initConversation)
      2. Gửi tin nhắn (webhook)
    """

    host = Config.BASE_URL
    wait_time = between(Config.WAIT_TIME_MIN, Config.WAIT_TIME_MAX)

    def on_start(self):
        self.payload_factory = PayloadFactory(
            bot_id=Config.DEFAULT_BOT_ID, messages=Config.MESSAGE_POOL
        )
        self.current_conversation_id = None
        self._init_conversation(first_init=True)

    def _init_conversation(self, first_init: bool = False):
        """Gọi API initConversation và cập nhật conversation_id."""
        payload = self.payload_factory.build_init_payload()
        with self.client.post(
            Config.INIT_ENDPOINT,
            json=payload.to_dict(),
            headers=Config.DEFAULT_HEADERS,
            name="POST /robot-ai-workflow/api/v1/bot/initConversation",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                self.current_conversation_id = payload.conversation_id
                response.success()
            else:
                response.failure(
                    f"Init failed: {response.status_code} -> {response.text}"
                )
                if first_init:
                    self.environment.events.request_failure.fire(
                        request_type="POST",
                        name="startup_init_conversation",
                        response_time=response.elapsed.total_seconds() * 1000
                        if response.elapsed
                        else 0,
                        response_length=len(response.content or b""),
                        exception=Exception("Failed to init conversation on startup"),
                    )

    def _send_webhook(self):
        """Gửi message tới webhook endpoint."""
        if not self.current_conversation_id:
            self._init_conversation()
            if not self.current_conversation_id:
                return

        payload = self.payload_factory.build_webhook_payload(
            conversation_id=self.current_conversation_id
        )

        with self.client.post(
            Config.WEBHOOK_ENDPOINT,
            json=payload.to_dict(),
            headers=Config.DEFAULT_HEADERS,
            name="POST /robot-ai-workflow/api/v1/bot/webhook",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
                try:
                    data = response.json()
                    status = data.get("status")
                    # Nếu bot báo END -> tạo conversation mới cho lượt kế tiếp.
                    if status and status.upper() == "END":
                        self.current_conversation_id = None
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(
                    f"Webhook failed: {response.status_code} -> {response.text}"
                )

    @task(Config.WEIGHT_INIT_CONVERSATION)
    def init_conversation_task(self):
        self._init_conversation()

    @task(Config.WEIGHT_WEBHOOK)
    def webhook_task(self):
        self._send_webhook()


