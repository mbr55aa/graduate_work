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
        """
        Find all info about the requested film
        @param search_str: film name
        @return: Film or None
        """
        film_uuid = self.find_film_uuid(search_str)
        film = self._get_film_by_uuid(film_uuid)
        return film

    def find_film_title(self, search_str: str) -> str:
        film = self.find_film_data(search_str)
        return getattr(film, 'title', None)

    def find_film_rating(self, search_str: str) -> str:
        film = self.find_film_data(search_str)
        return getattr(film, 'imdb_rating', None)

    def find_film_genres(self, search_str: str) -> List[str]:
        film = self.find_film_data(search_str)
        genres_names = []
        for genre in getattr(film, 'genre', []):
            genres_names.append(genre.name)
        return genres_names

    def find_film_directors(self, search_str: str) -> List[str]:
        """
        Find directors(s) of the requested film
        @param search_str: film name
        @return: list of directors' names or None
        """
        film = self.find_film_data(search_str)
        return getattr(film, 'directors_names', None)

    def find_film_actors(self, search_str: str) -> List[str]:
        """
        Find actors of the requested film
        @param search_str: film name
        @return: list of actors' names or  None
        """
        film = self.find_film_data(search_str)
        return getattr(film, 'actors_names', None)

    def find_film_description(self, search_str: str) -> List[str]:
        film = self.find_film_data(search_str)
        return getattr(film, 'description', None)

    def find_film_writers(self, search_str: str) -> List[str]:
        """
        Find writers of the requested film
        @param search_str: film name
        @return: list of writer's names or None
        """
        film = self.find_film_data(search_str)
        return getattr(film, 'writers_names', None)

    def find_film_uuid(self, search_str: str) -> Optional[UUID]:
        """
        Find UUID of the requested film
        @param search_str: film name
        @return: UUID of the film that best matches the request or None
        """
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
        """
        Get film data by UUID
        @param film_uuid: Film UUID
        @return: Film or None
        """
        response = self._get_response(f"film/{film_uuid}")
        if not response:
            return None
        return Film(**response)

    def _get_response(self, path: str, query: Optional[dict] = None) -> Optional[dict]:
        """
        Make response to Async API
        @param path: web path of response
        @param query: query params of GET request
        @return: data in JSON format
        """
        response = requests.get(self._get_api_url() + path, params=query)
        if response.status_code != HTTPStatus.OK:
            return None
        return json.loads(response.content.decode("UTF-8"))

    def _get_api_url(self) -> str:
        """
        Return URL of Async API
        @return: string with Async API URL
        """
        if not self.SEARCH_API_URL:
            self.SEARCH_API_URL = config.SEARCH_API_URL
        return self.SEARCH_API_URL

