"""Implements connector to Movie Async API for search info about movies, people, genres."""

import json
import requests
from typing import List
from uuid import UUID

from core import config
from models.film import Film


class SearchConnector:

    SEARCH_API_URL = None

    def __init__(self):
        pass

    def find_film_data(self, search_str: str) -> Film:
        film_uuid = self.find_film_uuid(search_str)
        film_data = self._get_film(film_uuid)
        return Film(**film_data)

    def find_film_directors(self, search_str: str) -> List[str]:
        film = self.find_film_data(search_str)
        return film.directors_names

    def find_film_actors(self, search_str: str) -> List[str]:
        film = self.find_film_data(search_str)
        return film.actors_names

    def find_film_writers(self, search_str: str) -> List[str]:
        film = self.find_film_data(search_str)
        return film.writers_names

    def find_film_uuid(self, search_str: str) -> UUID:
        request_str = 'film/search?query_string=' + search_str + '&page[size]=1'
        return self._get_response(request_str)[0].get('uuid')

    def _get_film(self, film_uuid: UUID) -> dict:
        request_str = 'film/' + film_uuid
        return self._get_response(request_str)

    def _get_response(self, request_str: str) -> dict:
        resp = requests.get(self._get_api_url() + request_str)
        return json.loads(resp.content.decode("UTF-8"))

    def _get_api_url(self) -> str:
        if not self.SEARCH_API_URL:
            self.SEARCH_API_URL = config.SEARCH_API_URL
        return self.SEARCH_API_URL

