import os


ALLOWED_HOSTS = os.getenv('ASSISTANT_ALLOWED_HOSTS', '0.0.0.0')
SEARCH_API_URL = os.getenv('SEARCH_API_URL', 'http://localhost:8000/api/v1/')
