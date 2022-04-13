"""Функции для запроса и вывода данных."""
import logging
import os
import random

import requests
from requests import Response

from assistant.speech_synthesis import SpeechSynthesis

logger = logging.getLogger(__name__)
assistant_url = os.getenv('ASSISTANT_URL', 'http://127.0.0.1:8001')

hello_dict = [
    'Здравствуй',
    'привет привет',
    'Привет, давно не виделись',
]

bye_dict = [
    'Ладно, пока',
    'Рада была помочь',
    'Будет скучно, обращайся',
]

failure_dict = [
    'К сожалению я не поняла',
    'А можешь повторить?',
    'Я наверное еще не умею это делать',
]

not_found_dict = [
    'По вашему запросу мне не удалось ничего найти',
]


def get_random_phrase(some_list: list) -> str:
    """
    Функция рандомного выбора фразы.
    :param some_list: Список возможных фраз.
    :return: Случайная фраза из списка.
    """
    response = random.choice(some_list)
    return response


def get_film_name(*args) -> tuple:
    """
    Функция получения имени кинопроизведения и его типа из парамтров запроса
    :param args: запрос от пользователя.
    :return: filmwork_name, filmwork_type: Имя и тип кинопроизведения.
    """
    # удаляем служебные слова 'фильм' 'сериал' 'картина' с любым предлогом перед ними
    types = ['фильм', 'картин', 'сериал', 'тв шоу']
    filmwork_type = 'фильм'
    for type in types:
        try:
            if type in args[0][0]:
                filmwork_type = type
                args[0].pop(0)
                break
            elif type in args[0][1]:
                filmwork_type = type
                args[0].pop(0)
                args[0].pop(0)
                break
        except:
            pass
    filmwork_name = ' '.join(args[0])
    return filmwork_name, filmwork_type


def play_greetings(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """
    Функция проигрывания приветствия помощника.
    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech(get_random_phrase(hello_dict))


def play_failure_phrase(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """
    Функция проигрывания ошибки распознавания команды.
    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech(get_random_phrase(failure_dict))


def play_farewell_and_quit(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """
    Функция проигрывания завершающей фразы и выхода программы.
    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech(get_random_phrase(bye_dict))
    exit(1)


def search_director(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """
    Функция поиска режиссера фильма.
    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    filmwork_name, filmwork_type = get_film_name(args[0])
    response = requests.get(f'{assistant_url}/api/v1/bob?method=find_film_directors&query={filmwork_name}')
    play_response(synthesizer, 'Режиссёр', response, filmwork_name, filmwork_type)


def search_actor(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """
    Функция поиска актера фильма.
    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    filmwork_name, filmwork_type = get_film_name(args[0])
    response = requests.get(f'{assistant_url}/api/v1/bob?method=find_film_actors&query={filmwork_name}')
    play_response(synthesizer, 'Актёры', response, filmwork_name, filmwork_type)


def play_response(synthesizer: SpeechSynthesis, role: str,
                  response: Response, filmwork_name: str, filmwork_type: str) -> None:
    """
    Функция проигрывания найденных актеров или режиссера кинопроизведения.
    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param role: Возможные доп. параметры.
    :param response: Ответ от assistant api.
    :param filmwork_name: Имя кинопроизведения.
    :param filmwork_type: Тип кинопроизведения.
    :return: None
    """
    try:
        result = response.json()
        if result == {'error': 'Not found'}:
            raise Exception
        synthesizer.play_voice_assistant_speech(f'{role} {filmwork_type}а {filmwork_name}: {result}')
    except:
        synthesizer.play_voice_assistant_speech(get_random_phrase(not_found_dict))


def play_help(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """
    Функция проигрывания фразы help.
    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech(
        'Ты можешь у меня спросить кто актер какого нибудь фильма, кто играл, '
        'кто сыграл либо сказать найди актера а так же можно спросить'
        'кто режиссёр какого нибудь фильма или сказать '
        'найди режиссера'
    )


def play_intro(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """
    Функция проигрывания вступления.
    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech(
        'Привет, я голосовой помощник Милена, если хочешь знать что '
        'я могу делать, спроси меня Что ты умеешь или просто помощь.'
        'Для завершения работы скажи хватит или пока'
    )
