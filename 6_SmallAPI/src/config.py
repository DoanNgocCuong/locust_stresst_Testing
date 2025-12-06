"""
Configuration module cho Locust test của Qwen3-1.7B API.
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


class Config:
    """Chứa các thông số cấu hình chính cho bài test."""

    # Base URL của API server
    BASE_URL = os.getenv(
        "QWEN_API_BASE_URL", "http://124.197.20.86:7862"
    )

    # API Endpoint
    CHAT_COMPLETIONS_ENDPOINT = os.getenv(
        "QWEN_API_CHAT_COMPLETIONS_ENDPOINT",
        "/v1/chat/completions",
    )

    # Model name
    MODEL_NAME = os.getenv(
        "QWEN_API_MODEL_NAME",
        "Qwen/Qwen3-1.7B",
    )

    # API Parameters
    TEMPERATURE = _get_float("QWEN_API_TEMPERATURE", 0.0)
    REPETITION_PENALTY = _get_float("QWEN_API_REPETITION_PENALTY", 1.1)
    STREAM = _get_bool("QWEN_API_STREAM", False)
    ENABLE_THINKING = _get_bool("QWEN_API_ENABLE_THINKING", False)

    # System prompt (có thể override từ env)
    SYSTEM_PROMPT = os.getenv(
        "QWEN_API_SYSTEM_PROMPT",
        "You are now intention detection. Given user's input, detect the suitable emotion and the need of celebrate for it.\n"
        "User input in format\n"
        "previous Question: string\n"
        "previous Answer: string\n"
        "Response to check: string to check\n\n"
        "You will extract the 'Response to check' and check:\n\n"
        "1. For emotion, pick from the list below:\n"
        "- happy, happy_2: when intention about happiness\n"
        "- calm: when intentionis to comfort\n"
        "- excited, excited_2: when expressing the exciting emotion\n"
        "- playful,playful_2,playful_3: intention about playing some fun activity\n"
        "- no_problem: intention when telling something is fine\n"
        "- encouraging,encouraging_2: intention when tell to try to do something\n"
        "- curious: intention when show curiousity\n"
        "- surprised: when being shocked or surprised\n"
        "- proud,proud_2: when showing proud\n"
        "- thats_right, thats_right_2: when telling something is correct\n"
        "- sad: when sad\n"
        "- angry: showing anger\n"
        "- worry: when show worriness\n"
        "- afraid: when feel scared\n"
        "- noisy: When intention about can't hear properly\n"
        "- thinking: intention about thinking\n\n"
        "2. For learn_score, if related to english learning\n"
        "- true: if question is about english learning, repeating something, and answer correctly\n"
        "- false: for other case include positive and negative\n\n\n"
        "return in single line json format.\n"
        '{"emotion":"<emotion name>","learn_score":true/flase}\n'
        "/no_think"
    )

    # Wait time giữa các requests (giây)
    WAIT_TIME_MIN = _get_float("QWEN_API_WAIT_MIN", 1.0)
    WAIT_TIME_MAX = _get_float("QWEN_API_WAIT_MAX", 3.0)

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

