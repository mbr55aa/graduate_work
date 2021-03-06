"""Модуль записи голоса"""
import logging
import os
from logging import config as logger_conf

from classifier.classifier import Classifier
from core.log_config import LOGGING
from recorder.recognizer import Recognizer
from termcolor import colored

from assistant.commands import config as commands
from assistant.connector import play_intro
from assistant.speech_synthesis import SpeechSynthesis

logger_conf.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def run_step():
    """Функция одного круга общения с голосовым помощником."""
    voice_input = recognizer.record_and_recognize_audio()
    if os.path.exists('microphone-results.wav'):
        os.remove('microphone-results.wav')
    logger.info(colored(voice_input, 'blue'))

    if voice_input:
        voice_input_parts = voice_input.split(' ')

        for guess in range(1, len(voice_input_parts) + 1):
            intent = classifier.get_intent((' '.join(voice_input_parts[0:guess])).strip())
            if intent:
                command_options = [voice_input_parts[guess:len(voice_input_parts)]]
                commands['intents'][intent]['responses'](synthesizer, *command_options)
                break
            elif guess == len(voice_input_parts):
                commands['failure_phrases'](synthesizer)


if __name__ == '__main__':

    logger.info('Работа программы началась')

    # Экземпляр класса записи и распознавания речи
    recognizer = Recognizer()
    # Экземпляр класса синтеза речи
    synthesizer = SpeechSynthesis()
    # Экземпляр класса классификатора запросов
    classifier = Classifier(commands)
    try:
        # Проигрываем вступление
        play_intro(synthesizer)
        while True:
            run_step()
    except KeyboardInterrupt:
        logger.info('Работа программы завершена')
