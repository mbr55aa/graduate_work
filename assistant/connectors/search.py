"""Implements connector to Movie Async API for search info about movies, people, genres."""

import json
import requests
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from core import config
from models.film import Film


class SearchConnector:

    SEARCH_API_URL = None

    def __init__(self):
        pass

    def find_film_data(self, search_str: str) -> Optional[Film]:
        film_uuid = self.find_film_uuid(search_str)
        film = self._get_film_by_uuid(film_uuid)
        return film

    def find_film_directors(self, search_str: str) -> List[str]:
        film = self.find_film_data(search_str)
        return getattr(film, 'directors_names', None)

    def find_film_actors(self, search_str: str) -> List[str]:
        film = self.find_film_data(search_str)
        return getattr(film, 'actors_names', None)

    def find_film_writers(self, search_str: str) -> List[str]:
        film = self.find_film_data(search_str)
        return getattr(film, 'writers_names', None)

    def find_film_uuid(self, search_str: str) -> Optional[UUID]:
        response = self._get_response(
            "film/search",
            query={
                "query_string": search_str,
                "page[size]": 1,
                "page[number]": 1,
            },
        )
        if not response:
            return None
        return response[0].get('uuid')

    def _get_film_by_uuid(self, film_uuid: UUID) -> Optional[Film]:
        response = self._get_response(f"film/{film_uuid}")
        if not response:
            return None
        return Film(**response)

    def _get_response(self, path: str, query: Optional[dict] = None) -> Optional[dict]:
        response = requests.get(self._get_api_url() + path, params=query)
        if response.status_code != HTTPStatus.OK:
            return None
        return json.loads(response.content.decode("UTF-8"))

    def _get_api_url(self) -> str:
        if not self.SEARCH_API_URL:
            self.SEARCH_API_URL = config.SEARCH_API_URL
        return self.SEARCH_API_URL

