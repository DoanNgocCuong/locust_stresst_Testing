"""
Configuration module cho Locust stress testing.
Chứa các cấu hình chung cho test suite.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file từ thư mục parent (3_ContextHandling_Robot/)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Class chứa các cấu hình cho Locust test."""
    
    # Base URL của API server - đọc từ .env file
    BASE_URL = os.getenv(
        '3_ContextHandling_Robot_URL',
        'http://103.253.20.30:30020'  # Default value nếu không có trong .env
    )
    
    # API Endpoints
    ENDPOINT_CONVERSATION_END = "/v1/conversations/end"
    ENDPOINT_ACTIVITIES_SUGGEST = "/v1/activities/suggest"
    
    # Headers mặc định
    DEFAULT_HEADERS = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Test data mặc định
    DEFAULT_BOT_ID = "talk_movie_preference"
    DEFAULT_BOT_NAME = "Movie Preference Talk"
    DEFAULT_BOT_TYPE = "dd"
    
    # Weight cho các task (tỷ lệ thực thi)
    WEIGHT_CONVERSATION_END = 1
    WEIGHT_ACTIVITIES_SUGGEST = 1

