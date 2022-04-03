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

    def get_settings(self, db_name):
        self.__settings = read_env_setting(db_name)
        if not self.__settings:
            self.__settings = AllSettings.parse_file('settings/settings.json')
            logger.info('Параметры считаны из файла settings.json')
            if db_name == 'es':
                return dict(self.__settings.film_work_es)
            elif db_name == 'pg':
                return dict(self.__settings.film_work_pg)
        return self.__settings


def read_env_setting(db_name):
    logger.info(db_name)
    if db_name == 'es':
        settings = read_env_es_setting()
    elif db_name == 'pg':
        settings = read_env_pg_setting()
        logger.info(settings)
    for value in settings.values():
        if not value:
            logger.error('Ошибка при попытке чтпния параметров из env.(Не все необходимые параметры объявлены.)')
            return None
    logger.info(f'Параметры успешно считаны из env. host:{settings["host"]}')
    return settings


def read_env_pg_setting():
    return dict(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
    )


def read_env_es_setting():
    return dict(
        host=os.getenv('ELASTIC_HOST'),
        port=os.getenv('ELASTIC_PORT'),
    )
