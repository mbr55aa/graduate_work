"""Функции для запроса и вывода данных."""
import random
from assistant.speech_synthesis import SpeechSynthesis

hello_dict = [
    'Здравствуй',
    'привет привет',
    'привет, давно не виделись',
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


def get_random_phrase(some_list: list) -> str:
    """
    Функция рандомного выбора фразы.
    :param some_list: Список возможных фраз.
    :return: Случайная фраза из списка.
    """
    response = random.choice(some_list)
    return response


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
    Функция проигрывания найденного режиссера фильма.
    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech('Режиссер фильма: вот')


def search_actor(synthesizer: SpeechSynthesis, *args: tuple) -> None:
    """
    Функция проигрывания найденного актера фильма.
    :param synthesizer: Экземпляр класса SpeechSynthesis.
    :param args: Возможные доп. параметры.
    :return: None
    """
    synthesizer.play_voice_assistant_speech('Актеры фильма: вот')


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
