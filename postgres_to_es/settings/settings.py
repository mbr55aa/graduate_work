from pydantic import BaseModel
import os
import logging

logger = logging.getLogger(__name__)


class PostgresSettings(BaseModel):
    host: str
    port: int
    dbname: str
    password: str
    user: str


class ElasticsearchSettings(BaseModel):
    host: str
    port: int


class AllSettings(BaseModel):
    film_work_pg: PostgresSettings
    film_work_es: ElasticsearchSettings


class Settings:

    __settings = None

    def get_settings(self):
        if not self.__settings:
            self.__settings = read_env_setting()
        return self.__settings


def read_env_setting():
    return AllSettings(
        film_work_pg=read_env_pg_setting(),
        film_work_es=read_env_es_setting(),
    )


def read_env_pg_setting():
    return PostgresSettings(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', 5432),
        dbname=os.getenv('POSTGRES_DB', 'postgres'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
    )


def read_env_es_setting():
    return ElasticsearchSettings(
        host=os.getenv('ELASTIC_HOST', 'localhost'),
        port=os.getenv('ELASTIC_PORT', 9200),
    )
