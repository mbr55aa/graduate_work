import os


ALLOWED_HOSTS = os.getenv('ASSISTANT_ALLOWED_HOSTS', '0.0.0.0')
