"""Класс голосовой помощник БОБ"""


class VoiceAssistant:
    """
    Настройки голосового ассистента, включающие имя, пол, язык речи, идентификатор.
    """
    name = None
    sex = None
    speech_language = None
    recognition_language = None
    voice_id = None

    def __init__(self, voice):
        """Функция инициализации экземпляра класса."""
        # установка голоса по умолчанию
        self.setup_assistant_voice(voice)

    def setup_assistant_voice(self, voice):
        """
        Установка голоса по умолчанию (индекс может меняться в
        зависимости от настроек операционной системы)
        """
        self.recognition_language = voice.languages
        self.sex = voice.gender
        self.name = voice.name
        self.voice_id = voice.id

