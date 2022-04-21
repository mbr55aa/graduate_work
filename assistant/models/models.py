from typing import List, Optional
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class AbstractModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PersonBase(AbstractModel):
    """Информация о персоне."""
    uuid: UUID
    full_name: str


class GenreBase(AbstractModel):
    """Информация о жанре."""
    uuid: UUID
    name: str


class FilmBase(AbstractModel):
    """Информация о фильме."""
    uuid: UUID
    title: str
    imdb_rating: float


class Film(AbstractModel):
    """Подробная информация о фильме."""
    uuid: UUID
    title: str
    imdb_rating: float
    description: str
    genre: Optional[List[GenreBase]]
    actors: Optional[List[PersonBase]]
    actors_names: Optional[List[str]]
    writers: Optional[List[PersonBase]]
    writers_names: Optional[List[str]]
    directors_names: Optional[List[str]]


class Films(AbstractModel):
    """Список фильмов."""
    genre: Optional[str]
    film_ids: Optional[FilmBase]


class Genre(AbstractModel):
    """Подробная информация о жанре."""
    uuid: UUID
    name: str
    description: Optional[str]
    film_ids: List[str]
    film_detailed_ids: Optional[List[Film]]


class Person(AbstractModel):
    """Подробная информация о персоне."""
    uuid: UUID
    full_name: str
    birth_date: Optional[str]
    film_ids: List[str]
    film_detailed_ids: Optional[List[Film]]
