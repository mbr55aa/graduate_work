from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class FilmPeople(BaseModel):
    uuid: UUID
    full_name: str


class FilmGenre(BaseModel):
    uuid: UUID
    name: str


class Film(BaseModel):
    """Подробная информация о фильме"""
    uuid: UUID
    title: str
    imdb_rating: float
    description: str
    genre: Optional[List[FilmGenre]]
    actors: Optional[List[FilmPeople]]
    actors_names: Optional[List[str]]
    writers: Optional[List[FilmPeople]]
    writers_names: Optional[List[str]]
    directors_names: Optional[List[str]]
