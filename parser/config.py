import logging

API_URL = "https://kinopoiskapiunofficial.tech/"
API_KEY = ""

POSTGRES_DB = "movies"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432


logging.basicConfig(
    format="%(levelname)s %(asctime)s: %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)
