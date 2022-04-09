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
    """
    {'kinopoiskId': 326, 'imdbId': 'tt0111161', 'nameRu': 'Побег из Шоушенка', 'nameEn': None, '
    nameOriginal': 'The Shawshank Redemption',
    'posterUrl': 'https://kinopoiskapiunofficial.tech/images/posters/kp/326.jpg',
    'posterUrlPreview': 'https://kinopoiskapiunofficial.tech/images/posters/kp_small/326.jpg',
    'coverUrl': 'https://avatars.mds.yandex.net/get-ott/1672343/2a0000016b03d1f5365474a90d26998e2a9f/orig',
    'reviewsCount': 586, 'ratingGoodReview': 92.7, 'ratingGoodReviewVoteCount': 517, 'ratingKinopoisk': 9.1,
    'ratingKinopoiskVoteCount': 823300, 'ratingImdb': 9.3, 'ratingImdbVoteCount': 2568406,
    'ratingFilmCritics': 8.4, 'ratingFilmCriticsVoteCount': 82, 'ratingAwait': None,
    'ratingAwaitCount': 2, 'ratingRfCritics': None, 'ratingRfCriticsVoteCount': 1,
    'webUrl': 'https://www.kinopoisk.ru/film/326/', 'year': 1994, 'filmLength': 142,
    'slogan': 'Страх - это кандалы. Надежда - это свобода',
    'description': 'Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника.',
    'shortDescription': 'Несправедливо осужденный банкир готовит побег из тюрьмы. Тим Роббинс в выдающейся',
    'editorAnnotation': None, 'isTicketsAvailable': False, 'productionStatus': None,
    'type': 'FILM', 'ratingMpaa': 'r', 'ratingAgeLimits': 'age16',
    'countries': [{'country': 'США'}], 'genres': [{'genre': 'драма'}],
    'startYear': None, 'endYear': None, 'serial': False, 'shortFilm': False, 'completed': False,
    'hasImax': False, 'has3D': False, 'lastSync': '2022-04-03T22:20:07.011482'}
    """
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
