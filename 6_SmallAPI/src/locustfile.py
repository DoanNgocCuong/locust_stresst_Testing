"""
Locust test cho Qwen3-1.7B API:
- API /v1/chat/completions

Mỗi user sẽ gửi requests ngẫu nhiên với các test cases khác nhau.
Hỗ trợ đọc dữ liệu từ file Excel (cột new_data) để stress test.

Tối ưu: Load Excel data 1 lần duy nhất và chia sẻ cho tất cả users.
"""

import json
from pathlib import Path
from locust import HttpUser, task, between

from config import Config
from data_generators import ChatCompletionPayloadFactory
from excel_data_loader import get_shared_loader


# Load Excel data 1 lần duy nhất khi module được import (trước khi Locust chạy)
# Điều này đảm bảo không tính thời gian load vào response time
_shared_excel_loader = None
if Config.EXCEL_DATA_PATH:
    excel_file = Path(Config.EXCEL_DATA_PATH)
    if excel_file.exists():
        _shared_excel_loader = get_shared_loader(str(excel_file))
        if _shared_excel_loader:
            print(f"✅ [Module Init] Đã load {_shared_excel_loader.get_data_count()} dòng dữ liệu từ Excel (chia sẻ cho tất cả users)")
    else:
        print(f"⚠️  [Module Init] File Excel không tồn tại: {Config.EXCEL_DATA_PATH}")


class QwenAPIUser(HttpUser):
    """
    Mỗi Locust user tương ứng với 1 client mô phỏng.
    User sẽ gửi requests tới API chat/completions với test data ngẫu nhiên.
    """

    host = Config.BASE_URL
    wait_time = between(Config.WAIT_TIME_MIN, Config.WAIT_TIME_MAX)

    def on_start(self):
        """
        Method được gọi khi một user instance bắt đầu.
        Khởi tạo payload factory cho user này.
        Sử dụng shared Excel loader đã được load sẵn (không load lại).
        """
        # Sử dụng shared loader đã được load sẵn (không load lại)
        # Điều này đảm bảo không tính thời gian load vào response time
        use_excel_data = _shared_excel_loader is not None
        
        self.payload_factory = ChatCompletionPayloadFactory(
            excel_loader=_shared_excel_loader,
            use_excel_data=use_excel_data
        )

    def _check_response_success(self, response):
        """
        Helper method để kiểm tra response có thành công không.

        Args:
            response: Locust response object

        Returns:
            bool: True nếu response thành công, False nếu không
        """
        if response.status_code == 200:
            try:
                # Kiểm tra response có phải JSON hợp lệ không
                data = response.json()
                # Kiểm tra có field 'choices' trong response (format của OpenAI API)
                if "choices" in data:
                    response.success()
                    return True
                else:
                    response.failure(
                        f"Response missing 'choices' field. Response: {response.text[:500]}"
                    )
                    return False
            except json.JSONDecodeError:
                response.failure(f"Invalid JSON response: {response.text[:500]}")
                return False
        else:
            response.failure(
                f"Unexpected status code: {response.status_code}. "
                f"Response: {response.text[:500]}"
            )
            return False

    @task
    def test_chat_completions(self):
        """
        Task test API /v1/chat/completions.
        
        Test việc gửi request để detect emotion và learn_score từ user input.
        """
        # Generate payload động
        payload = self.payload_factory.build_payload()

        # Gửi POST request
        with self.client.post(
            Config.CHAT_COMPLETIONS_ENDPOINT,
            json=payload.to_dict(),
            headers=Config.DEFAULT_HEADERS,
            catch_response=True,
            name="POST /v1/chat/completions",
        ) as response:
            # Kiểm tra response
            self._check_response_success(response)

