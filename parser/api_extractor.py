import time

import requests

from config import API_KEY, API_URL, logger


def make_request(path, query=None):
    logger.info(f"Request to {API_URL + path}...")
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(API_URL + path, headers=headers, params=query)
    response.raise_for_status()
    return response


def get_top_250_films():
    """
    {'filmId': 435, 'nameRu': 'Зеленая миля', 'nameEn': 'The Green Mile', 'year': '1999',
    'filmLength': '03:09', 'countries': [{'country': 'США'}],
    'genres': [{'genre': 'драма'}, {'genre': 'криминал'}, {'genre': 'детектив'}
    'rating': '9.1', 'ratingVoteCount': 754886,
    'posterUrl': 'https://kinopoiskapiunofficial.tech/images/posters/kp/435.jpg',
    'posterUrlPreview': 'https://kinopoiskapiunofficial.tech/images/posters/kp_small/435.jpg',
    'ratingChange': None}
    """
    films = []
    last_page = False
    page = 1
    max_pages = 100  # todo: del after debug

    while not last_page and page <= max_pages:
        try:
            response = make_request(
                "api/v2.2/films/top", query={"type": "TOP_250_BEST_FILMS", "page": page}
            )
            res = response.json()
        except Exception as err:
            logger.error(err)
            last_page = True
            continue

        if len(res["films"]) == 0:
            last_page = True
            continue

        films.extend(res["films"])

        page += 1
        time.sleep(2)

    return films


def get_film_by_id(film_id):
    try:
        response = make_request(f"api/v2.2/films/{film_id}")
        return response.json()
    except Exception as err:
        logger.error(err)


def get_person_by_film_id(film_id):
    """
    [{'staffId': 24262, 'nameRu': 'Фрэнк Дарабонт', 'nameEn': 'Frank Darabont', 'description': None,
    'posterUrl': 'https://kinopoiskapiunofficial.tech/images/actor_posters/kp/24262.jpg',
    'professionText': 'Режиссеры', 'professionKey': 'DIRECTOR'},
    """

    try:
        response = make_request(f"api/v1/staff", {"filmId": film_id})
        return response.json()
    except Exception as err:
        logger.error(err)
