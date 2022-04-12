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

    def __init__(self, voice: dict):
        """
        Функция инициализации экземпляра класса.
        :param voice: Голос, полученный из инструмента синтеза речи
        """
        self.voice = voice
        self.setup_assistant_voice()

    def setup_assistant_voice(self):
        """Установка голоса."""
        self.recognition_language = self.voice.languages
        self.sex = self.voice.gender
        self.name = self.voice.name
        self.voice_id = self.voice.id
