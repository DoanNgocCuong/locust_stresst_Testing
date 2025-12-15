"""
Configuration module cho Locust test của Qwen3-0.6B API.
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


def _get_bool(env_name: str, default: bool) -> bool:
    """Helper để đọc bool từ env (fallback nếu có lỗi)."""
    value = os.getenv(env_name)
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes", "on")


def _get_list(env_name: str, default: list[str]) -> list[str]:
    """
    Helper để đọc list từ env, tách bằng dấu phẩy.
    Trả về default nếu không tồn tại hoặc chuỗi rỗng.
    """
    value = os.getenv(env_name)
    if value is None or value.strip() == "":
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


class Config:
    """Chứa các thông số cấu hình chính cho bài test."""

    # Base URL của API server
    BASE_URL = os.getenv(
        "QWEN_API_BASE_URL", "http://103.253.20.30:30030"
    )

    # API Endpoint
    CHAT_COMPLETIONS_ENDPOINT = os.getenv(
        "QWEN_API_CHAT_COMPLETIONS_ENDPOINT",
        "/v1/chat/completions",
    )

    # Model name
    MODEL_NAME = os.getenv(
        "QWEN_API_MODEL_NAME",
        "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
    )

    # Giới hạn token cho câu trả lời
    MAX_TOKENS = _get_int("QWEN_API_MAX_TOKENS", 5)

    # Stop tokens cho API
    STOP_TOKENS = _get_list("QWEN_API_STOP_TOKENS", ["\n", " ", ".", ","])

    # API Parameters
    TEMPERATURE = _get_float("QWEN_API_TEMPERATURE", 0.0)
    REPETITION_PENALTY = _get_float("QWEN_API_REPETITION_PENALTY", 1.0)
    STREAM = _get_bool("QWEN_API_STREAM", False)
    ENABLE_THINKING = _get_bool("QWEN_API_ENABLE_THINKING", False)

    # System prompt (có thể override từ env)
    SYSTEM_PROMPT = os.getenv(
        "QWEN_API_SYSTEM_PROMPT",
        "You are an emotion classifier for Pika Robot's responses.\n"
        "Task:\n"
        "* Read the conversation snippet.\n"
        "* Focus ONLY on \"Now Pika Robot's Response need check\" and identify the MAIN emotion expressed in that turn.\n\n"
        "Emotion rules:\n"
        "Choose exactly ONE emotion from this list and output only that word:\n"
        "happy, calm, excited, playful, no_problem, encouraging, curious, surprised, proud, thats_right, sad, angry, worry, afraid, noisy, thinking"
    )

    # Wait time giữa các requests (giây)
    WAIT_TIME_MIN = _get_float("QWEN_API_WAIT_MIN", 1)
    WAIT_TIME_MAX = _get_float("QWEN_API_WAIT_MAX", 3)

    # Headers mặc định
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
    }

    # Đường dẫn file Excel chứa dữ liệu stress test (cột new_data)
    # Mặc định: file result_all_rows.xlsx trong thư mục data
    EXCEL_DATA_PATH = os.getenv(
        "EXCEL_DATA_PATH",
        str(Path(__file__).resolve().parent.parent / "data" / "result_all_rows.xlsx")
    )

