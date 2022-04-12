import random
from string import Template
from typing import List, Union

INTRO = (
    'Привет! Вы находитесь в приватном навыке "Кинотеатр Практикума". '
    "Скажите, какую информацию о фильме или персоне вы хотите найти. "
    'Для подсказки спросите "Что ты умеешь?"'
)
REPEAT = "Ох, я забыла, что нужно повторить. Попросите меня лучше что-нибудь найти."
HELP = (
    "Например, вы можете узнать информацию о фильме, "
    "искать кино по жанрами, найти режиссера или актеров."
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

FILM_DESCRIPTION = "$film. $description. Рейтинг $rating. "


def get_phrase(phrase: Union[List, str], **kwargs) -> str:
    template_string = random.choice(phrase) if isinstance(phrase, List) else phrase
    result = Template(template_string).substitute(**kwargs)
    return result
