"""Запись и распознавание речи."""

import logging
import speech_recognition

logger = logging.getLogger(__name__)


class Recognaizer:
    """Класс записи и распознавания речи."""

    microphone = None
    recognizer = None

    def __init__(self):
        """Функция инициализации экземпляра класса."""
        # инициализация инструментов распознавания и ввода речи
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()

    def record_and_recognize_audio(self, *args: tuple):
        """Запись и распознавание аудио."""
        with self.microphone:
            recognized_data = ""

            # регулирование уровня окружающего шума
            self.recognizer.adjust_for_ambient_noise(self.microphone, duration=2)

            try:
                logger.info("Listening...")
                audio = self.recognizer.listen(self.microphone, 5, 5)

                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())

            except speech_recognition.WaitTimeoutError:
                logger.error("Can you check if your microphone is on, please?")
                return

            # использование online-распознавания через Google
            try:
                logger.info("Started recognition...")
                recognized_data = self.recognizer.recognize_google(audio, language="ru").lower()

            except speech_recognition.UnknownValueError:
                logger.exception('Can\'t recognize data.')

            # в случае проблем с доступом в Интернет происходит выброс ошибки
            except speech_recognition.RequestError:
                logger.error("Check your Internet Connection, please.")

            return recognized_data
