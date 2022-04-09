"""Запись и распознавание речи."""

import json
import logging
import os
import wave
from typing import Optional

import speech_recognition
from termcolor import colored
from vosk import Model, KaldiRecognizer

from bob.core.config import VOSK_MODEL

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

    def use_offline_recognition(self) -> str:
        """
        Переключение на оффлайн-распознавание речи
        :return: распознанная фраза
        """
        recognized_data = ""
        try:
            # проверка наличия модели на нужном языке в каталоге приложения
            if not os.path.exists(f'models/{VOSK_MODEL}'):
                print(colored("Please download the model from:\n"
                              "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.",
                              "red"))
                exit(1)

            # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
            wave_audio_file = wave.open('microphone-results.wav', 'rb')
            model = Model(f'models/{VOSK_MODEL}')
            offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())
            data = wave_audio_file.readframes(wave_audio_file.getnframes())
            if len(data) > 0:
                if offline_recognizer.AcceptWaveform(data):
                    recognized_data = offline_recognizer.Result()
                    # получение данных распознанного текста из JSON-строки (чтобы можно было выдать по ней ответ)
                    recognized_data = json.loads(recognized_data)
                    recognized_data = recognized_data['text']
        except BaseException:
            logger.exception('Offline recognition exception')
            print(colored('Sorry, speech service is unavailable. Try again later', 'red'))

        return recognized_data

    def record_and_recognize_audio(self, *args: tuple) -> Optional[str]:
        """
        Запись и распознавание аудио.
        :param args: Дополнительные аргументы.
        :return: recognized_data: Распознанная речь.
        """
        with self.microphone:
            recognized_data = ''

            # регулирование уровня окружающего шума
            self.recognizer.adjust_for_ambient_noise(self.microphone, duration=2)

            try:
                logger.info('Listening...')
                audio = self.recognizer.listen(self.microphone, 5, 5)

                with open('microphone-results.wav', 'wb') as file:
                    file.write(audio.get_wav_data())

            except speech_recognition.WaitTimeoutError:
                logger.error('Can you check if your microphone is on, please?')
                return None

            # использование online-распознавания через Google
            try:
                logger.info('Started recognition...')
                recognized_data = self.recognizer.recognize_google(audio, language='ru').lower()

            except speech_recognition.UnknownValueError:
                logger.exception('Can\'t recognize data.')

            # в случае проблем с доступом в Интернет происходит попытка использовать offline-распознавание через Vosk
            except speech_recognition.RequestError:
                print(colored('Trying to use offline recognition...', 'cyan'))
                recognized_data = self.use_offline_recognition()

            return recognized_data
