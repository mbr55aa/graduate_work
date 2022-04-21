from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class PersonBase(BaseModel):
    """Информация о персоне."""
    uuid: UUID
    full_name: str


class GenreBase(BaseModel):
    """Информация о жанре."""
    uuid: UUID
    name: str


class FilmBase(BaseModel):
    """Информация о фильме."""
    uuid: UUID
    title: str
    imdb_rating: float


class Film(BaseModel):
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


class Films(BaseModel):
    """Список фильмов."""
    genre: Optional[str]
    film_ids: Optional[FilmBase]


class Genre(BaseModel):
    """Подробная информация о жанре."""
    uuid: UUID
    name: str
    description: Optional[str]
    film_ids: List[str]
    film_detailed_ids: Optional[List[Film]]


class Genre(BaseModel):
    """Подробная информация о жанре."""
    uuid: UUID
    name: str
    description: Optional[str]
    film_ids: List[str]
    film_detailed_ids: Optional[List[Film]]


class Person(BaseModel):
    """Подробная информация о персоне."""
    uuid: UUID
    full_name: str
    birth_date: Optional[str]
    film_ids: List[str]
    film_detailed_ids: Optional[List[Film]]
