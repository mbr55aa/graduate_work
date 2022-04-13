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
            genre=", ".join([genre.name for genre in film.genre]) if film.genre else "",
            description=film.description,
            rating=film.imdb_rating,
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
    """Ищет топ фильмов, фильмы по жанрам."""
    is_next = form["slots"].get("next", {}).get("value")

    if is_next:
        if "page" not in current_state:
            return (
                "Попросите меня найти лучшие фильмы или картины определенного жанра",
                current_state,
            )
        current_state["page"] += 1
    else:
        api_req = {
            "genre": form["slots"].get("genre", {}).get("value"),
        }
        # api_req = {k: v for k, v in api_req.items() if v}
        current_state.update({**api_req, "page": 1})

    films = api.find_top_films(
        genre_id=current_state.get("genre"), page=current_state["page"]
    )

    if not films:
        return "Я не смогла найти ни одного фильма", current_state

    return (
        ". ".join(
            [film.title + ", рейтинг " + str(film.imdb_rating) for film in films]
        ),
        current_state,
    )


if __name__ == "__main__":
    # print(get_film({"slots": {"film": {"value": "Брат"}}}, {}))
    # print(get_director({"slots": {"film": {"value": "Брат"}}}, {}))
    # print(get_actor({"slots": {"film": {"value": "Брат"}}}, {}))
    state = {}
    print(
        get_films(
            {"slots": {"genre": {"value": "03caf522-1ab4-4785-aba7-bbecb70d8963"}}},
            state,
        )
    )
    print(get_films({"slots": {"next": {"value": "1"}}}, state))
    print(get_films({"slots": {"next": {"value": "1"}}}, state))
