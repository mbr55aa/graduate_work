"""Настройки боба."""
import os

VOSK_MODEL = os.getenv('VOSK_MODEL', 'vosk-model-small-ru-0.22')
ASSISTANT_URL = os.getenv('ASSISTANT_URL', 'http://localhost:8001/api/v1/bob/')
# Возможные типы кинопроизведений
fw_types: list = ['фильм', 'сериал', 'тв шоу']
