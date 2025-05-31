"""
Configuration settings for the Novel Companion AI application
"""
import os

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT = 30

# Application Settings
DEFAULT_PAGE_CONFIG = {
    "page_title": "Novel Companion AI",
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# UI Configuration
MAX_CHAT_MESSAGES = 50
DEFAULT_ANALYSIS_DEPTH = 3
SUPPORTED_FILE_TYPES = ["txt", "pdf", "epub"]
MAX_FILE_SIZE_MB = 10 