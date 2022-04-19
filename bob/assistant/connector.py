"""Функции для запроса и вывода данных."""
import logging
import random
from http import HTTPStatus
from typing import Optional, Tuple

import requests
from core.config import ASSISTANT_URL, fw_types
from requests import Response
from termcolor import colored

from assistant.context import Context
from assistant.phrases import (bye_dict, failure_dict, hello_dict,
                               not_found_dict)
from assistant.speech_synthesis import SpeechSynthesis

logger = logging.getLogger(__name__)


def get_random_phrase(some_list: list) -> str:
    """Функция рандомного выбора фразы.
    
    :param some_list: Список возможных фраз.
    :return: Случайная фраза из списка.
    """
    response = random.choice(some_list)
    return response


def get_response(resp_str: str) -> Optional[Response]:
    """Функция запроса к assistant API.
    
    :param resp_str: Строка запроса.
    :return: response либо None.
    """
    try:
        response = requests.get(resp_str)
    except requests.exceptions.ConnectionError:
        logger.error(colored('Can\'t connect to assistant api', 'red'))
        return None
    else:
        if response.status_code != HTTPStatus.OK:
            return None
        return response


def get_filmwork_name_from_api(filmwork_name: str) -> Optional[str]:
    """Функция запроса корректного имени кинопроизведения из assistant API.
    
    :param filmwork_name: Предпологаемое имя кинопроизведения.
    :return: Корректное имя или None.
    """
    filmwork_name_resp = get_response(
        f'{ASSISTANT_URL}?method=find_film_title&query={filmwork_name}'
    )
    if filmwork_name_resp:
        return filmwork_name_resp.json()
    return None


def get_film_name(*args) -> Tuple[str, str]:
    """Функция получения имени кинопроизведения и его типа из параметров запроса.

    :param args: запрос от пользователя.
    :return: Tuple(filmwork_name, filmwork_type): Имя и тип кинопроизведения.
    """
    # Если пользователь не произносит тип кинопроизведения, то по умолчанию считаем фильмом
    filmwork_type: str = 'фильм'
    # Из запроса пользователя получаем тип кинопроизведения и имя (если есть)
    index: int = 0
    for word in args[0]:
        for fw_type in fw_types:
            if fw_type in word:
                index = args[0].index(word) + 1
                filmwork_type = fw_type
    filmwork_name = ' '.join([args[0][i] for i in range(index, len(args[0]))])

    # Пытаемся получить корректное имя кинопроизведения из API
    # (проверка существования, исправление ошибок)
    filmwork_name = get_filmwork_name_from_api(filmwork_name)

    # Если в запросе пользователя содержался тип кинопроизведения (index > 0), то он спрашивал
    # про конректное кинопроизведение, значит брать последнее успешное имя из контекста не нужно
    # и контекст обнуляем.
    if filmwork_name:
        Context.put_name_to_context(filmwork_name)
    elif index > 0:
        Context.put_name_to_context(None)
    else:
        filmwork_name = Context.get_name_from_context()

    return filmwork_name, filmwork_type


def play_greetings(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция проигрывания приветствия помощника.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech(get_random_phrase(hello_dict))


def play_failure_phrase(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция проигрывания ошибки распознавания команды.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech(get_random_phrase(failure_dict))


def play_farewell_and_quit(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция проигрывания завершающей фразы и выхода программы.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech(get_random_phrase(bye_dict))
    exit(1)


def search_director(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция поиска режиссера кинопроизведения.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    filmwork_name, filmwork_type = get_film_name(args[0])
    response = get_response(f'{ASSISTANT_URL}?method=find_film_directors&query={filmwork_name}')
    synthesizer.play_voice_assistant_speech(f'Ищу режиссера {filmwork_type}а {filmwork_name}')
    play_response(synthesizer, 'Режиссёр', response, filmwork_name, filmwork_type)
    # synthesizer.play_voice_assistant_speech(f'Ищу режиссера')


def search_writer(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция поиска сценариста кинопроизведения.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    filmwork_name, filmwork_type = get_film_name(args[0])
    response = get_response(f'{ASSISTANT_URL}?method=find_film_writers&query={filmwork_name}')
    synthesizer.play_voice_assistant_speech(f'Ищу Сценариста {filmwork_type}а {filmwork_name}')
    play_response(synthesizer, 'Сценарист', response, filmwork_name, filmwork_type)
    # synthesizer.play_voice_assistant_speech(f'Ищу Сценариста')


def search_actor(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция поиска актеров кинопроизведения.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    filmwork_name, filmwork_type = get_film_name(args[0])
    response = get_response(f'{ASSISTANT_URL}?method=find_film_actors&query={filmwork_name}')
    synthesizer.play_voice_assistant_speech(f'Ищу Актёров {filmwork_type}а {filmwork_name}')
    play_response(synthesizer, 'Актёры', response, filmwork_name, filmwork_type)
    # synthesizer.play_voice_assistant_speech(f'Ищу Актёров')


def search_description(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция поиска описания кинопроизведения.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    filmwork_name, filmwork_type = get_film_name(args[0])
    response = get_response(f'{ASSISTANT_URL}?method=find_film_description&query={filmwork_name}')
    synthesizer.play_voice_assistant_speech(f'Ищу описание {filmwork_type}а {filmwork_name}')
    play_response(synthesizer, 'Описание', response, filmwork_name, filmwork_type)
    # synthesizer.play_voice_assistant_speech(f'Ищу описание')


def search_rating(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция поиска рейтинга кинопроизведения.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    filmwork_name, filmwork_type = get_film_name(args[0])
    response = get_response(f'{ASSISTANT_URL}?method=find_film_rating&query={filmwork_name}')
    synthesizer.play_voice_assistant_speech(f'Ищу рейтинг {filmwork_type}а {filmwork_name}')
    play_response(synthesizer, 'Рейтинг', response, filmwork_name, filmwork_type)
    # synthesizer.play_voice_assistant_speech(f'Ищу рейтинг')


def search_genres(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция поиска жанров кинопроизведения.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    filmwork_name, filmwork_type = get_film_name(args[0])
    response = get_response(f'{ASSISTANT_URL}?method=find_film_genres&query={filmwork_name}')
    synthesizer.play_voice_assistant_speech(f'Ищу жанры {filmwork_type}а {filmwork_name}')
    play_response(synthesizer, 'Жанры', response, filmwork_name, filmwork_type)
    # synthesizer.play_voice_assistant_speech(f'Ищу жанры')


def play_response(synthesizer: SpeechSynthesis, role: str,
                  response: Optional[Response], filmwork_name: str, filmwork_type: str) -> None:
    """Функция проигрывания найденных результатов по кинопроизведению.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param role: Тип ответа.
    :param response: Ответ от assistant api.
    :param filmwork_name: Имя кинопроизведения.
    :param filmwork_type: Тип кинопроизведения.
    :return: None
    """
    if response:
        result = response.json()
        synthesizer.play_voice_assistant_speech(f'{role} {filmwork_type}а {filmwork_name}: {result}')
        return
    synthesizer.play_voice_assistant_speech(get_random_phrase(not_found_dict))


def play_help(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция проигрывания фразы help.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech(
        'Ты можешь у меня спросить:'
        '\n Кто? актер какого-нибудь фильма. Кто играл? Кто сыграл? Либо сказать найди актера. '
        '\nА так же можно спросить: Кто? режиссёр какого нибудь фильма. '
        '\nИли сказать: Найди режиссера. Найди сценариста. Расскажи про фильм.'
    )
    # synthesizer.play_voice_assistant_speech('помощь')


def play_intro(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """Функция проигрывания вступления.

    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech(
        'Привет, я голосовой помощник Милена.'
        '\n Если хочешь узнать что? я умею делать, просто спроси меня:'
        '\n Что ты умеешь? '
        '\n Или скажи: Помощь.'
        '\n Для завершения работы, скажи: Хватит Или Пока.'
    )
    # synthesizer.play_voice_assistant_speech('вступление')
