"""Модели жанров."""

from typing import List, Optional
from uuid import UUID

from models._base import OrjsonModel


class GenreAPI(OrjsonModel):
    """
    Информация о жанре: Идентификатор, имя, описание, список фильмов
    """
    uuid: UUID
    name: str
    description: Optional[str]
    film_ids: List[str]


class GenreBriefAPI(OrjsonModel):
    """
    Сокращенная информация о жанре: Идентификатор, имя, описание
    """
    uuid: UUID
    name: str
    description: Optional[str]


class Genre(OrjsonModel):
    """
    Информация о жанре
    """
    uuid: UUID
    name: str
    description: Optional[str]
    films: List[dict]


class GenreBrief(OrjsonModel):
    """
    Краткая информация о жанре без списка фильмов.
    Для возврата списка всех жанров фильма
    """
    id: UUID
    name: str
    description: Optional[str]
