"""Класс контекст запросов пользователя."""
from typing import Optional


class Context:
    """Класс контекст запросов."""
    filmwork = None
    actors = None
    director = None
    writer = None
    description = None

    @staticmethod
    def put_name_to_context(filmwork_name: Optional[str]) -> None:
        """Функция для запоминания корректного имени кинопроизведения в контексте.

        :param filmwork_name: корректное имя кинопроизведения.
        :return: None
        """
        Context.filmwork = filmwork_name

    @staticmethod
    def get_name_from_context() -> str:
        """Функция для извлечения из контекста послднего корректного имени кинопроизведения.

        :return: filmwork_name: корректное имя кинопроизведения.
        """
        return Context.filmwork
