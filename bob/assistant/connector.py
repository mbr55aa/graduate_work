"""Функции для запроса и вывода данных"""


def play_greetings(synthesizer, *args: tuple):
    synthesizer.play_voice_assistant_speech('Здравствуй')


def play_failure_phrase(synthesizer, *args: tuple):
    synthesizer.play_voice_assistant_speech('К сожалению я не поняла')


def play_farewell_and_quit(synthesizer, *args: tuple):
    synthesizer.play_voice_assistant_speech('Ладно, пока')
    exit(1)


def search_director(synthesizer, *args: tuple):
    synthesizer.play_voice_assistant_speech('Режиссер фильма: вот')


def search_actor(synthesizer, *args: tuple):
    synthesizer.play_voice_assistant_speech('Актеры фильма: вот')


def play_help(synthesizer, *args: tuple):
    synthesizer.play_voice_assistant_speech('Ты можешь у меня спросить кто актер какого нибудь фильма, кто играл, '
                                            'кто сыграл либо сказать найди актера а так же можно спросить'
                                            'кто режиссёр какого нибудь фильма кто снял фильм или сказать '
                                            'найди режиссера')


def play_intro(synthesizer):
    synthesizer.play_voice_assistant_speech('Привет, я голосовой помощник Милена, если хочешь знать что '
                                            'я могу делать, спроси меня Что ты умеешь или просто помощь.'
                                            'Для завершения работы скажи хватит или пока')
