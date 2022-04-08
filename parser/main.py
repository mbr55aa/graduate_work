import time

import postgres_loader as db
from api_extractor import (get_film_by_id, get_person_by_film_id,
                           get_top_250_films)
from config import logger


def main():

    db.truncate_all_tables()

    logger.info("Get top 250 films...")
    films = get_top_250_films()

    genres_log = {}
    persons_log = {}
    allowed_roles = ["DIRECTOR", "ACTOR", "WRITER"]

    for film in films:

        full_info = get_film_by_id(film["filmId"])

        try:
            id = db.add_filmwork(full_info)
        except Exception as e:
            logger.error("Could not add film_work", e)
            continue

        # genres
        for genre in film["genres"]:
            genre_name = genre["genre"]

            if genre_name not in genres_log:
                genre_id = db.add_genre(genre)
                genres_log[genre_name] = genre_id
            else:
                genre_id = genres_log[genre_name]

            db.add_genre_film_work(genre_id, id)

        # persons
        persons = get_person_by_film_id(film["filmId"])

        for person in persons[:20]:
            role = person["professionKey"]
            staff_id = person["staffId"]

            if role in allowed_roles and person["nameRu"] != "":
                if staff_id not in persons_log:
                    person_id = db.add_person(person)
                    persons_log[staff_id] = person_id
                else:
                    person_id = persons_log[staff_id]

                db.add_person_film_work(person_id, id, role)

        time.sleep(2)

    db.close_session()


if __name__ == "__main__":
    main()
