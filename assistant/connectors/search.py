"""Implements connector to Movie Async API for search info about movies, people, genres."""

import json
import requests
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from core import config
from core.utils import LackOfParamsError
from models.models import Film, FilmBase, Films, Genre, Person


class SearchConnector:

    SEARCH_API_URL = None

    # Film methods
    def find_film_data(self, search_str: str) -> Optional[Film]:
        """Find all info about the requested film.

        :param search_str: film name
        :return: Film or None
        """
        film_uuid = self._find_film_uuid(search_str)
        film = self._get_film_by_uuid(film_uuid)
        return film

    def find_film_title(self, search_str: str) -> str:
        """Find title of the requested film.

        :param search_str: film name
        :return: Title or None
        """
        film = self.find_film_data(search_str)
        return getattr(film, 'title', None)

    def find_film_rating(self, search_str: str) -> str:
        """Find rating of the requested film.

        :param search_str: film name
        :return: rating or None
        """
        film = self.find_film_data(search_str)
        return getattr(film, 'imdb_rating', None)

    def find_film_genres(self, search_str: str) -> List[str]:
        """Find genres of the requested film.

        :param search_str: film name
        :return: Genres or None
        """
        film = self.find_film_data(search_str)
        genres_names = []
        for genre in getattr(film, 'genre', []):
            genres_names.append(genre.name)
        return genres_names

    def find_film_directors(self, search_str: str) -> List[str]:
        """Find directors(s) of the requested film.

        :param search_str: film name
        :return: list of directors' names or None
        """
        film = self.find_film_data(search_str)
        return getattr(film, 'directors_names', None)

    def find_film_actors(self, search_str: str) -> List[str]:
        """Find actors of the requested film.

        :param search_str: film name
        :return: list of actors' names or  None
        """
        film = self.find_film_data(search_str)
        return getattr(film, 'actors_names', None)

    def find_film_description(self, search_str: str) -> str:
        """Find description of the requested film.

        :param search_str: film name
        :return: Description or None
        """
        film = self.find_film_data(search_str)
        return getattr(film, 'description', None)

    def find_film_writers(self, search_str: str) -> List[str]:
        """Find writers of the requested film.

        :param search_str: film name
        :return: list of writer's names or None
        """
        film = self.find_film_data(search_str)
        return getattr(film, 'writers_names', None)

    # Films methods
    def find_top_films(self, search_str=None):
        films = Films()
        if search_str:
            genre_uuid = self._find_genre_uuid(search_str)
            genre = self._get_genre_by_uuid(genre_uuid)
            films.genre = genre.name
        else:
            genre_uuid = None
        film_ids = self._get_films(genre_uuid)
        films.film_ids = film_ids
        return films

    # Genre methods
    def find_genre_data(self, search_str):
        genre_id = self._find_genre_uuid(search_str)
        genre = self._get_genre_by_uuid(genre_id, detailed=True)
        return genre

    def find_genre_films(self, search_str: str) -> List[str]:
        genre = self.find_genre_data(search_str)
        return [f.title for f in getattr(genre, 'film_detailed_ids', [])]

    # Person methods
    def find_person_data(self, search_str: str) -> Person:
        """Find information about requested person.

        :param search_str: person name
        :return: Person
        """
        person_id = self._find_person_uuid(search_str)
        person = self._get_person_by_uuid(person_id, detailed=True)
        return person

    def find_person_name(self, search_str: str) -> str:
        """Find person name.

        :param search_str: person name
        :return: person full name
        """
        person = self.find_person_data(search_str)
        return getattr(person, 'full_name', None)

    def find_person_films(self, search_str: str) -> List[str]:
        """Find films with person.

        :param search_str: person name
        :return: list of films
        """
        person = self.find_person_data(search_str)
        return [f.title for f in getattr(person, 'film_detailed_ids', [])]

    # Support methods
    def _find_film_uuid(self, search_str: str) -> Optional[UUID]:
        """Find UUID of the requested film.

        :param search_str: film name
        :return: UUID of the film that best matches the request or None
        """
        if not search_str:
            raise LackOfParamsError
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
        """Get film data by UUID.

        :param film_uuid: Film UUID
        :return: Film or None
        """
        response = self._get_response(f"film/{film_uuid}")
        if not response:
            return None
        return Film(**response)

    def _get_films(self, genre_uuid: Optional[UUID]):
        response = self._get_response(
            "film/",
            query={
                "filter[genre]": genre_uuid,
                "page[size]": 10,
                "page[number]": 1,
            },
        )
        if not response:
            return None
        return [FilmBase(**row) for row in response]

    def _find_genre_uuid(self, search_str):
        if not search_str:
            raise LackOfParamsError
        response = self._get_response(
            "genre/",
            query={
                "search[name]": search_str,
                "page[size]": 1,
                "page[number]": 1,
            },
        )
        if not response:
            return None
        return response[0].get('uuid')

    def _get_genre_by_uuid(self, genre_uuid, detailed=False):
        response = self._get_response(f"genre/{genre_uuid}")
        if not response:
            return None
        genre = Genre(**response)
        if not detailed:
            return genre
        genre.film_detailed_ids = []
        for film_uuid in response['film_ids'] or []:
            film = self._get_film_by_uuid(film_uuid)
            if film:
                genre.film_detailed_ids.append(film)
        return genre

    def _find_person_uuid(self, search_str: str) -> Optional[UUID]:
        """Find UUID of the requested person.

        :param search_str: person name
        :return: UUID of the person that best matches the request or None
        """
        if not search_str:
            raise LackOfParamsError
        response = self._get_response(
            "person/",
            query={
                "search[name]": search_str,
                "page[size]": 1,
                "page[number]": 1,
            },
        )
        if not response:
            return None
        return response[0].get('uuid')

    def _get_person_by_uuid(self, person_uuid: UUID, detailed=False) -> Optional[Person]:
        """Get person data by UUID.

        :param person_uuid: Person UUID
        :return: Person or None
        """
        response = self._get_response(f"person/{person_uuid}")
        if not response:
            return None
        person = Person(**response)
        if not detailed:
            return person
        person.film_detailed_ids = []
        for film_uuid in response['film_ids'] or []:
            film = self._get_film_by_uuid(film_uuid)
            if film:
                person.film_detailed_ids.append(film)
        return person

    def _get_response(self, path: str, query: Optional[dict] = None) -> Optional[dict]:
        """Make response to Async API.

        :param path: web path of response
        :param query: query params of GET request
        :return: data in JSON format
        """
        response = requests.get(self._get_api_url() + path, params=query)
        if response.status_code != HTTPStatus.OK:
            return None
        return json.loads(response.content.decode("UTF-8"))

    def _get_api_url(self) -> str:
        """Get URL of Async API.

        :return: string with Async API URL
        """
        if not self.SEARCH_API_URL:
            self.SEARCH_API_URL = config.SEARCH_API_URL
        return self.SEARCH_API_URL
