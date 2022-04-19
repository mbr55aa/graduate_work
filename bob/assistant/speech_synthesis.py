"""Класс синтеза речи"""
import logging

import pyttsx3  # синтез речи (Text-To-Speech)
from termcolor import colored

from assistant.voice_assistant import VoiceAssistant

logger = logging.getLogger(__name__)


class SpeechSynthesis:
    """Класс синтеза речи."""
    ttsEngine = None

    def __init__(self):
        """Функция инициализации экземпляра класса."""
        # инициализация инструмента синтеза речи
        self.ttsEngine = pyttsx3.init()
        # выбираем русский голос (27)
        voice = self.ttsEngine.getProperty('voices')[27]
        self.ttsEngine.setProperty('voice', voice.id)
        self.assistant = VoiceAssistant(voice)

    def play_voice_assistant_speech(self, text_to_speech: str):
        """Проигрывание речи ответов голосового ассистента (без сохранения аудио).

        :param text_to_speech: текст, который нужно преобразовать в речь
        """
        logger.info(colored(text_to_speech, 'green'))
        self.ttsEngine.say(str(text_to_speech))
        self.ttsEngine.runAndWait()
