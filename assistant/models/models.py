from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class BasePerson(BaseModel):
    """Информация о персоне."""
    uuid: UUID
    full_name: str


class BaseGenre(BaseModel):
    """Информация о жанре."""
    uuid: UUID
    name: str


class Film(BaseModel):
    """Подробная информация о фильме."""
    uuid: UUID
    title: str
    imdb_rating: float
    description: str
    genre: Optional[List[BaseGenre]]
    actors: Optional[List[BasePerson]]
    actors_names: Optional[List[str]]
    writers: Optional[List[BasePerson]]
    writers_names: Optional[List[str]]
    directors_names: Optional[List[str]]


class Genre(BaseModel):
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
