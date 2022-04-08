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
