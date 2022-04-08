import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Date, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TimestampMixin(object):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)


class UpdatedMixin(object):
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)


class FilmWork(TimestampMixin, UpdatedMixin, Base):
    __tablename__ = "film_work"
    __table_args__ = {"schema": "content"}

    title = Column(String)
    description = Column(String)
    creation_date = Column(String)
    certificate = Column(String)
    file_path = Column(String)
    rating = Column(Float)
    type = Column(String, default="movie")


class Genre(TimestampMixin, UpdatedMixin, Base):
    __tablename__ = "genre"
    __table_args__ = {"schema": "content"}

    name = Column(String)


class Person(TimestampMixin, UpdatedMixin, Base):
    __tablename__ = "person"
    __table_args__ = {"schema": "content"}

    full_name = Column(String)
    birth_date = Column(Date)


class GenreFilmWork(TimestampMixin, Base):
    __tablename__ = "genre_film_work"
    __table_args__ = {"schema": "content"}

    film_work_id = Column(UUID(as_uuid=True), ForeignKey("content.film_work.id"))
    genre_id = Column(UUID(as_uuid=True), ForeignKey("content.genre.id"))


class PersonFilmWork(TimestampMixin, Base):
    __tablename__ = "person_film_work"
    __table_args__ = {"schema": "content"}

    film_work_id = Column(UUID(as_uuid=True), ForeignKey("content.film_work.id"))
    person_id = Column(UUID(as_uuid=True), ForeignKey("content.person.id"))
    role = Column(String)
