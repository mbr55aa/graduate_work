import logging
from logging import config as logger_conf

from flask import Flask

from api.v1.alice import blueprint_alice
from api.v1.bob import blueprint_bob
from core import config
from core.log_config import LOGGING


logger_conf.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


app = Flask(__name__)

app.register_blueprint(blueprint_alice)
app.register_blueprint(blueprint_bob)


def main():
    logger.info('Starting')
    app.run(debug=True, host=config.ALLOWED_HOSTS, port=8001)


if __name__ == '__main__':
    main()
