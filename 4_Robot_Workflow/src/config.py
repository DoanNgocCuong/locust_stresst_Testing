"""
Configuration module cho Locust test của Robot Workflow.
Hỗ trợ đọc cấu hình từ file .env ở thư mục dự án.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# Tải .env (nếu tồn tại) ở thư mục cha
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


def _get_float(env_name: str, default: float) -> float:
    """Helper để đọc float từ env (fallback nếu có lỗi)."""
    value = os.getenv(env_name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _get_int(env_name: str, default: int) -> int:
    """Helper để đọc int từ env (fallback nếu có lỗi)."""
    value = os.getenv(env_name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


class Config:
    """Chứa các thông số cấu hình chính cho bài test."""

    BASE_URL = os.getenv("ROBOT_WORKFLOW_BASE_URL", "http://103.253.20.30:30000")

    INIT_ENDPOINT = os.getenv(
        "ROBOT_WORKFLOW_INIT_ENDPOINT",
        "/robot-ai-workflow/api/v1/bot/initConversation",
    )
    WEBHOOK_ENDPOINT = os.getenv(
        "ROBOT_WORKFLOW_WEBHOOK_ENDPOINT",
        "/robot-ai-workflow/api/v1/bot/webhook",
    )

    DEFAULT_BOT_ID = _get_int("ROBOT_WORKFLOW_BOT_ID", 3)
    DEFAULT_INIT_MESSAGE = os.getenv("ROBOT_WORKFLOW_INIT_MESSAGE", "sẵn sàng")

    WAIT_TIME_MIN = _get_float("ROBOT_WORKFLOW_WAIT_MIN", 1.0)
    WAIT_TIME_MAX = _get_float("ROBOT_WORKFLOW_WAIT_MAX", 3.0)

    WEIGHT_INIT_CONVERSATION = _get_int(
        "ROBOT_WORKFLOW_WEIGHT_INIT", 1
    )
    WEIGHT_WEBHOOK = _get_int("ROBOT_WORKFLOW_WEIGHT_WEBHOOK", 3)

    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    RAW_MESSAGE_POOL = os.getenv("ROBOT_WORKFLOW_MESSAGE_POOL")
    MESSAGE_POOL = (
        [
            msg.strip()
            for msg in RAW_MESSAGE_POOL.split("|")
            if msg.strip()
        ]
        if RAW_MESSAGE_POOL
        else [
            "sẵn sàng",
            "cho mình thử thử thách tiếp theo",
            "mình cần ví dụ chi tiết hơn",
            "có thể giải thích kỹ hơn không",
            "mình muốn kết thúc buổi học",
            "hãy đánh giá đáp án của mình",
            "mình muốn luyện tập thêm",
        ]
    )


