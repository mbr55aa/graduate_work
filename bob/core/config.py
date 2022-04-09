"""Настройки боба."""
import os

URL = os.getenv('URL', 'https://some_url')
VOSK_MODEL = os.getenv('VOSK_MODEL', 'vosk-model-small-ru-0.22')
