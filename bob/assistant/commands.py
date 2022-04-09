"""Список команд, которые обрабатывает голосовой помощник."""
from assistant.connector import play_greetings, play_failure_phrase, search_director, \
  search_actor, play_farewell_and_quit, play_help

config = {
  'intents': {
    'greeting': {
      'examples': [
        'привет',
        'здравствуй',
        'добрый день',
        'доброе утро',
        'добрый вечер',
        'хай'
      ],
      'responses': play_greetings
    },
    'farewell': {
      'examples': [
        'пока',
        'увидимся',
        'до встречи',
        'хватит',
      ],
      'responses': play_farewell_and_quit
    },
    'search_actor': {
      'examples': [
        'найди актёра',
        'кто актёр',
        'кто играл',
        'кто сыграл',
      ],
      'responses': search_actor
    },
    'search_director': {
      'examples': [
        'найди режиссёра',
        'кто режиссёр',
        'кто автор',
        'кто снял',
        'кто снимал',
      ],
      'responses': search_director
    },
    'help': {
      'examples': [
        'что ты умеешь',
        'что ты мошежь',
        'что спросить',
        'помощь',
      ],
      'responses': play_help
    },
  },
  'failure_phrases': play_failure_phrase
}
