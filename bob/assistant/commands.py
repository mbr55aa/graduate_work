"""Список команд, которые обрабатывает голосовой помощник."""
from assistant.connector import (play_failure_phrase, play_farewell_and_quit,
                                 play_greetings, play_help, search_actor,
                                 search_description, search_director,
                                 search_genres, search_rating, search_writer)

config = {
    'intents': {
        'greeting': {
            'examples': [
                'привет',
                'здравствуй',
                'здравствуйте',
                'добрый день',
                'доброе утро',
                'добрый вечер',
                'приветствую',
            ],
            'responses': play_greetings
        },
        'farewell': {
            'examples': [
                'спасибо пока',
                'ладно пока',
                'пока',
                'увидимся',
                'до встречи',
                'хватит',
                'выключи',
                'выход',
            ],
            'responses': play_farewell_and_quit
        },
        'search_actor': {
            'examples': [
                'найди актёров',
                'найди актёра',
                'актёр',
                'кто актёр',
                'кто играл',
                'кто сыграл',
                'играл',
            ],
            'responses': search_actor
        },
        'search_director': {
            'examples': [
                'найди режиссёра',
                'режиссёр',
                'автор',
                'снимал',
                'кто режиссёр',
                'кто автор',
                'кто снял',
                'кто снимал',
            ],
            'responses': search_director
        },
        'search_writer': {
            'examples': [
                'найди сценариста',
                'сценарист',
                'сценарий',
                'кто сценарист',
                'кто написал сценарий',
                'чей сценарий',
            ],
            'responses': search_writer
        },
        'seacrh_film_info': {
            'examples': [
                'расскажи про',
                'расскажи о чём',
                'описание',
                'аннотация',
                'аннотацию',
                'содержание',
                'про что',
                'о чём',
            ],
            'responses': search_description
        },
        'seacrh_film_genres': {
            'examples': [
                'найди жанр',
                'какой жанр',
                'какого жанра',
                'какие жанры',
                'жанр',
                'жанры',
            ],
            'responses': search_genres
        },
        'seacrh_film_rating': {
            'examples': [
                'найди рейтинг',
                'какой рейтинг',
                'скажи рейтинг',
                'рейтинг',
            ],
            'responses': search_rating
        },
        'help': {
            'examples': [
                'расскажи что ты умеешь',
                'что ты умеешь',
                'расскажи что ты мошежь',
                'что ты мошежь',
                'что можно спросить',
                'как ты работаешь',
                'помощь',
                'помоги',
            ],
            'responses': play_help
        },
    },
    'failure_phrases': play_failure_phrase
}
