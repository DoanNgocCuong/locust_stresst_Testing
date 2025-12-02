"""
Locust stress test file cho Context Handling Robot APIs.
Test 2 endpoints:
1. /v1/conversations/end - Kết thúc conversation
2. /v1/activities/suggest - Gợi ý activities
"""

from locust import HttpUser, task, between

from config import Config
from data_generators import (
    ConversationDataGenerator,
    ActivitySuggestDataGenerator
)


class ContextHandlingRobotUser(HttpUser):
    """
    Locust User class định nghĩa các task test cho Context Handling Robot APIs.
    
    Tuân thủ Single Responsibility: Class này chỉ chịu trách nhiệm định nghĩa
    các task và thực thi HTTP requests.
    """
    
    # Thời gian chờ giữa các task (1-3 giây)
    wait_time = between(1, 3)
    
    # Các status codes được coi là success
    # 200: OK
    # 201: Created
    # 202: Accepted (cho async APIs - request đã được chấp nhận và đang xử lý)
    SUCCESS_STATUS_CODES = [200, 201, 202]
    
    def on_start(self):
        """
        Method được gọi khi một user instance bắt đầu.
        Có thể dùng để setup initial state nếu cần.
        """
        pass
    
    def _check_response_success(self, response):
        """
        Helper method để kiểm tra response có thành công không.
        
        Args:
            response: Locust response object
            
        Returns:
            bool: True nếu response thành công, False nếu không
        """
        if response.status_code in self.SUCCESS_STATUS_CODES:
            response.success()
            return True
        else:
            response.failure(
                f"Unexpected status code: {response.status_code}. "
                f"Response: {response.text[:500]}"  # Giới hạn độ dài để tránh log quá dài
            )
            return False
    
    @task(Config.WEIGHT_CONVERSATION_END)
    def test_conversation_end(self):
        """
        Task test API /v1/conversations/end.
        
        Test việc gửi request kết thúc conversation với đầy đủ conversation logs.
        API này trả về 202 (Accepted) vì là async processing.
        """
        # Generate payload động
        payload = ConversationDataGenerator.generate_conversation_end_payload()
        
        # Gửi POST request
        with self.client.post(
            Config.ENDPOINT_CONVERSATION_END,
            json=payload,
            headers=Config.DEFAULT_HEADERS,
            catch_response=True,
            name="POST /v1/conversations/end"
        ) as response:
            # Kiểm tra response (chấp nhận 200, 201, 202)
            self._check_response_success(response)
    
    @task(Config.WEIGHT_ACTIVITIES_SUGGEST)
    def test_activities_suggest(self):
        """
        Task test API /v1/activities/suggest.
        
        Test việc gửi request để lấy gợi ý activities cho user.
        """
        # Generate payload động
        payload = ActivitySuggestDataGenerator.generate_activity_suggest_payload()
        
        # Gửi POST request
        with self.client.post(
            Config.ENDPOINT_ACTIVITIES_SUGGEST,
            json=payload,
            headers=Config.DEFAULT_HEADERS,
            catch_response=True,
            name="POST /v1/activities/suggest"
        ) as response:
            # Kiểm tra response (chấp nhận 200, 201, 202)
            self._check_response_success(response)

