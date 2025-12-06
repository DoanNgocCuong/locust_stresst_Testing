"""
Locust stress test cho câu SQL:

    SELECT id, name, description, task_chain, generation_params,
           provider_name, system_prompt, format_output
    FROM llm_bot
    WHERE id = 373;

Mục tiêu:
- Đo thời gian thực thi query dưới tải đồng thời.
- Xem khả năng scale của DB (PostgreSQL) khi nhiều client cùng query.
"""

from locust import User, task, between, events

from db_client import PostgresClient


class SqlUser(User):
    """
    Mỗi Locust user tương ứng với 1 DB client (1 connection).
    User sẽ:
      - Mở connection khi start
      - Liên tục thực thi cùng một câu SQL
      - Đóng connection khi stop
    """

    wait_time = between(0.1, 0.5)  # có thể chỉnh tuỳ bài test

    def on_start(self) -> None:
        self.client_db = PostgresClient()
        try:
            self.client_db.connect()
        except Exception as exc:  # pragma: no cover - defensive
            # Báo lỗi cho Locust dashboard
            events.request_failure.fire(
                request_type="SQL",
                name="connect",
                response_time=0,
                response_length=0,
                exception=exc,
            )

    def on_stop(self) -> None:
        if hasattr(self, "client_db"):
            self.client_db.close()

    @task
    def run_select_llm_bot(self) -> None:
        """
        Task chính: thực thi câu SELECT cần stress test.
        Kết quả sẽ hiển thị trên Locust dashboard như 1 request type 'SQL'.
        """
        try:
            result = self.client_db.execute_query()
            events.request_success.fire(
                request_type="SQL",
                name="SELECT llm_bot WHERE id = 373",
                response_time=result.duration_ms,
                response_length=result.rows,
            )
        except Exception as exc:
            events.request_failure.fire(
                request_type="SQL",
                name="SELECT llm_bot WHERE id = 373",
                response_time=0,
                response_length=0,
                exception=exc,
            )







