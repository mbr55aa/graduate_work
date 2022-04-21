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


class FilmPeople(AbstractModel):
    uuid: UUID
    full_name: str


class FilmGenre(AbstractModel):
    uuid: UUID
    name: str


class Film(AbstractModel):
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

    def __getitem__(self, item):
        return item
