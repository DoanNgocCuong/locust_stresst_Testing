"""
Config module cho stress test SQL.
Đọc cấu hình kết nối DB và câu query từ .env hoặc giá trị mặc định.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


class DbConfig:
    """Thông tin kết nối database (PostgreSQL)."""

    HOST: str = os.getenv("SQL_DB_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("SQL_DB_PORT", "5432"))
    NAME: str = os.getenv("SQL_DB_NAME", "postgres")
    USER: str = os.getenv("SQL_DB_USER", "postgres")
    PASSWORD: str = os.getenv("SQL_DB_PASSWORD", "postgres")

    CONNECT_TIMEOUT: int = int(os.getenv("SQL_DB_CONNECT_TIMEOUT", "5"))
    # Số kết nối tối đa mỗi Locust user (ở đây dùng 1/ user để đơn giản)


class QueryConfig:
    """Cấu hình câu SQL sẽ được stress test."""

    # Cho phép override từ env nếu cần
    RAW_QUERY: str = os.getenv(
        "SQL_STRESS_QUERY",
        (
            "SELECT id, name, description, task_chain, generation_params, "
            "provider_name, system_prompt, format_output "
            "FROM llm_bot WHERE id = 373;"
        ),
    )







