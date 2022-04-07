"""Implements connector to Movie Async API for search info about movies, people, genres."""

import json
import requests
from uuid import UUID

from core import config


class SearchConnector:

    SEARCH_API_URL = None

    def __init__(self):
        pass

    def find_film_director(self, search_str: str) -> str:
        film_uuid = self.find_film(search_str)
        film_data = self._get_film(film_uuid)
        return film_data

    def find_film(self, search_str: str) -> UUID:
        return self._get_response(search_str)[0].get('uuid')

    def _get_film(self, film_uuid):
        pass

    def _get_response(self, get_params):
        resp = requests.get(self._get_api_url() + 'film/search?query_string=' + get_params + '&page[size]=1&page[number]=1')
        return json.loads(resp.content.decode("UTF-8"))

    def _get_api_url(self):
        if not self.SEARCH_API_URL:
            self.SEARCH_API_URL = config.SEARCH_API_URL
        return self.SEARCH_API_URL

