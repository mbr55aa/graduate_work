import os

ALLOWED_HOSTS = os.getenv('ASSISTANT_ALLOWED_HOSTS', '0.0.0.0')
SEARCH_API_URL = os.getenv('SEARCH_API_URL', 'http://localhost:8000/api/v1/')
LOG_LEVEL = os.getenv('ASSISTANT_LOG_LEVEL', 'DEBUG')
LOG_FILE = os.getenv('ASSISTANT_LOG_FILE', 'assistant.log')
