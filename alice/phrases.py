import random
from string import Template
from typing import List, Union

INTRO = (
    'Привет! Вы находитесь в приватном навыке "Кинотеатр Практикума". '
    "Скажите, какую информацию о фильме или персоне вы хотите найти. "
    "Для подсказки спросите, что ты умеешь?"
)
REPEAT = "Ох, я забыла, что нужно повторить. Попросите меня лучше что-нибудь найти."
HELP = (
    "Например, вы можете узнать информацию о фильме, "
    "искать популярное кино по жанрами, найти режиссера или актера любого фильма."
)
UNSUCCESSFUL = [
    "Хьюстон, у нас проблемы! Кажется я такое не умею.",
    "Я не поняла, спросите что-нибудь другое.",
]
EXIT = (
    "Приятно было поискать для вас! "
    'Чтобы вернуться в навык, скажите "Запусти навык Кинотеатр Практикума". До свидания!'
)

DIRECTOR = "$film снял $director"

ACTORS = [
    "В картине $film приняли участие $actors",
    "В фильме $film снимались $actors",
]

FILM_DESCRIPTION = "$film. $genre. $description. Рейтинг $rating."

PERSON = "Имя $person можно найти в титрах таких фильмов, как $film."

FILMS = [
    "Могу порекомендовать $film.",
    "Попробуйте посмотреть $film.",
    "Вам могут понравиться $film.",
]


def get_phrase(phrase: Union[List, str], **kwargs) -> str:
    """
    Подставляет в шаблон ответа переменные,
    если вариантов ответа несколько — возвращает случайный.
    """
    template_string = random.choice(phrase) if isinstance(phrase, List) else phrase
    result = Template(template_string).substitute(**kwargs)
    return result
