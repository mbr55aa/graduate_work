import logging

import psycopg2
import psycopg2.extras
from psycopg2 import DatabaseError
from resources import backoff
from settings.settings import Settings

logger = logging.getLogger(__name__)


class PGLoader(Settings):
    __pg_con = None
    __cursor = None

    def do_query(self, sql: str):
        try:
            self.__get_cursor().execute(sql)
            return self.__cursor.fetchall()
        except DatabaseError:
            self.__pg_con.close()
            self.__cursor = None

    @backoff()
    def __get_cursor(self):
        if not self.__cursor:
            self.__pg_con = psycopg2.connect(**self.__get_db_params())
            logger.info('Успешно подключено к БД Postgres')
            self.__cursor = self.__pg_con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return self.__cursor

    def __get_db_params(self):
        return dict(self.get_settings().film_work_pg)
