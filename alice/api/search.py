"""Implements connector to Movie Async API for search info about movies, people, genres."""

from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

import requests

from .models import Film, FilmBase, Genre


class SearchConnector:
    def __init__(self, url):
        self._url = url

    def _get_response(self, path: str, query: Optional[dict] = None) -> Optional[dict]:
        response = requests.get(self._url + path, params=query)
        return response

    def find_film_data(self, search_str: str) -> Optional[Film]:
        film_uuid = self._find_film_uuid(search_str)
        film = self._get_film_by_uuid(film_uuid)
        return film

    def find_film_directors(self, search_str: str):
        film = self.find_film_data(search_str)
        if not film:
            return None, None
        return film.title, ", ".join(film.directors_names)

    def find_film_actors(self, search_str: str, limit: int = 5):
        film = self.find_film_data(search_str)
        if not film:
            return None, None
        return film.title, ", ".join(film.actors_names[:limit])

    def find_top_films(
        self, genre_id: Optional[UUID], page: int = 1
    ) -> Optional[List[FilmBase]]:
        films = self._find_films(genre_id=genre_id, page=page)
        return films

    def _find_film_uuid(self, search_str: str) -> Optional[UUID]:
        response = self._get_response(
            "film/search",
            query={
                "query_string": search_str,
                "page[size]": 1,
                "page[number]": 1,
            },
        )
        if response.status_code != HTTPStatus.OK:
            return None

        return response.json()[0]["uuid"]

    def _get_film_by_uuid(self, film_uuid: UUID) -> Optional[Film]:
        response = self._get_response(f"film/{film_uuid}")
        if response.status_code != HTTPStatus.OK:
            return None

        return Film(**response.json())

    def _find_films(
        self, genre_id: Optional[UUID], page: int = 1, size: int = 5
    ) -> Optional[List[FilmBase]]:
        response = self._get_response(
            "film/",
            query={
                "filter[genre]": genre_id,
                "page[size]": size,
                "page[number]": page,
            },
        )
        if response.status_code != HTTPStatus.OK:
            return None

        return [FilmBase(**row) for row in response.json()]

    def _find_genres(self, page: int = 1, size: int = 100) -> Optional[List[Genre]]:
        response = self._get_response(
            "genre/",
            query={
                "page[size]": size,
                "page[number]": page,
            },
        )
        if response.status_code != HTTPStatus.OK:
            return None

        return [Genre(**row) for row in response.json()]
