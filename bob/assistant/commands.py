"""Список команд, которые обрабатывает голосовой помощник."""
from assistant.connector import play_greetings, play_failure_phrase, search_director, \
  search_actor, play_farewell_and_quit

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
        'кто снял',
      ],
      'responses': search_director
    }
  },
  'failure_phrases': play_failure_phrase
}
