import random
from typing import Optional

import phrases
from api.fake_db import fake_persons_db
from api.models import Film
from api.search import SearchConnector
from phrases import get_phrase

api = SearchConnector("http://51.250.26.192:8000/api/v1/")


def get_director(form, current_state):
    """Ищет режиссера по названию фильма."""
    api_req = {
        "film": form["slots"].get("film", {}).get("value"),
    }
    api_req = {k: v for k, v in api_req.items() if v}
    current_state.update(api_req)

    if "film" not in current_state:
        return "Кажется, я не знаю про какой фильм идет речь", current_state

    film_name, directors_names = api.find_film_directors(current_state["film"])
    if not film_name:
        return "К сожалению, я не смогла найти этот фильм", current_state

    if not directors_names:
        return (
            "К сожалению, я не нашла режиссера фильма " + film_name,
            current_state,
        )

    return (
        get_phrase(phrases.DIRECTOR, film=film_name, director=directors_names),
        current_state,
    )


def get_film(form, current_state) -> Optional[Film]:
    """Ищет фильм по названию и рассказывает о нем информацию."""
    api_req = {
        "film": form["slots"].get("film", {}).get("value"),
    }
    api_req = {k: v for k, v in api_req.items() if v}
    current_state.update(api_req)

    if "film" not in current_state:
        return "Кажется, я не знаю про какой фильм идет речь", current_state

    film = api.find_film_data(current_state["film"])
    if not film:
        return "К сожалению, я не смогла найти этот фильм", current_state

    return (
        get_phrase(
            phrases.FILM_DESCRIPTION,
            film=film.title,
            rating=film.imdb_rating,
            description=film.description,
        ),
        current_state,
    )


def get_actor(form, current_state):
    """Ищет актеров по названию фильма."""
    api_req = {
        "film": form["slots"].get("film", {}).get("value"),
    }
    api_req = {k: v for k, v in api_req.items() if v}
    current_state.update(api_req)

    if "film" not in current_state:
        return "Уточните еще раз фильм", current_state

    film_name, actors_names = api.find_film_actors(current_state["film"])
    if not film_name:
        return "К сожалению, я не смогла найти этот фильм", current_state

    if not actors_names:
        return (
            "К сожалению, я нашла актеров фильма " + film_name,
            current_state,
        )

    return (
        get_phrase(phrases.ACTORS, film=film_name, actors=actors_names),
        current_state,
    )


def get_films(form, current_state):
    """Ищет топ фильмов, возможно по жанрам."""
    # api_req = {
    #     "film": form["slots"].get("film", {}).get("value"),
    # }
    # api_req = {k: v for k, v in api_req.items() if v}
    # current_state.update(api_req)

    films = api.find_top_films(page=1)
    if not films:
        return "Я не смогла найти фильмы", current_state

    return (
        ". ".join(
            [film.title + ", рейтинг " + str(film.imdb_rating) for film in films]
        ),
        current_state,
    )


# if __name__ == "__main__":
#     print(get_film({"slots": {"film": {"value": "Брат"}}}, {}))
#     print(get_director({"slots": {"film": {"value": "Брат"}}}, {}))
#     print(get_actor({"slots": {"film": {"value": "Брат"}}}, {}))
