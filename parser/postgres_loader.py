from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                    POSTGRES_PORT, POSTGRES_USER)

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
