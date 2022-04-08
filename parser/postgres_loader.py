from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                    POSTGRES_PORT, POSTGRES_USER)
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

db_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(db_string)
Session = sessionmaker(bind=engine)
session = Session()


def truncate_all_tables():
    """Truncate all tables"""
    session.execute("""TRUNCATE TABLE content.film_work""")
    session.execute("""TRUNCATE TABLE content.genre""")
    session.execute("""TRUNCATE TABLE content.genre_film_work""")
    session.execute("""TRUNCATE TABLE content.person""")
    session.execute("""TRUNCATE TABLE content.person_film_work""")
    session.commit()


def close_session():
    session.close()


# {'kinopoiskId': 326, 'imdbId': 'tt0111161', 'nameRu': 'Побег из Шоушенка', 'nameEn': None, '
# nameOriginal': 'The Shawshank Redemption',
# 'posterUrl': 'https://kinopoiskapiunofficial.tech/images/posters/kp/326.jpg',
# 'posterUrlPreview': 'https://kinopoiskapiunofficial.tech/images/posters/kp_small/326.jpg',
# 'coverUrl': 'https://avatars.mds.yandex.net/get-ott/1672343/2a0000016b03d1f5365474a90d26998e2a9f/orig',
# 'reviewsCount': 586, 'ratingGoodReview': 92.7, 'ratingGoodReviewVoteCount': 517, 'ratingKinopoisk': 9.1,
# 'ratingKinopoiskVoteCount': 823300, 'ratingImdb': 9.3, 'ratingImdbVoteCount': 2568406,
# 'ratingFilmCritics': 8.4, 'ratingFilmCriticsVoteCount': 82, 'ratingAwait': None,
# 'ratingAwaitCount': 2, 'ratingRfCritics': None, 'ratingRfCriticsVoteCount': 1,
# 'webUrl': 'https://www.kinopoisk.ru/film/326/', 'year': 1994, 'filmLength': 142,
# 'slogan': 'Страх - это кандалы. Надежда - это свобода',
# 'description': 'Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника.',
# 'shortDescription': 'Несправедливо осужденный банкир готовит побег из тюрьмы. Тим Роббинс в выдающейся',
# 'editorAnnotation': None, 'isTicketsAvailable': False, 'productionStatus': None,
# 'type': 'FILM', 'ratingMpaa': 'r', 'ratingAgeLimits': 'age16',
# 'countries': [{'country': 'США'}], 'genres': [{'genre': 'драма'}],
# 'startYear': None, 'endYear': None, 'serial': False, 'shortFilm': False, 'completed': False,
# 'hasImax': False, 'has3D': False, 'lastSync': '2022-04-03T22:20:07.011482'}
def add_filmwork(row):
    film = FilmWork(
        title=row["nameRu"],
        description=row["shortDescription"],
        rating=row["ratingImdb"],
    )

    session.add(film)
    session.commit()
    return film.id


def add_genre(row):
    genre = Genre(
        name=row["genre"].capitalize(),
    )

    session.add(genre)
    session.commit()
    return genre.id


def add_genre_film_work(genre_id, film_work_id):
    genre_film_work = GenreFilmWork(genre_id=genre_id, film_work_id=film_work_id)

    session.add(genre_film_work)
    session.commit()
    return genre_film_work.id


def add_person(row):
    person = Person(full_name=row["nameRu"])

    session.add(person)
    session.commit()
    return person.id


def add_person_film_work(person_id, film_work_id, role):
    person_film_work = PersonFilmWork(
        person_id=person_id, film_work_id=film_work_id, role=role.lower()
    )

    session.add(person_film_work)
    session.commit()
    return person_film_work.id
