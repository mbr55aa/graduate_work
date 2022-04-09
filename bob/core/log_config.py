"""Настроуки логгера."""

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': LOG_FORMAT,
        },
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': LOG_FORMAT,
        },
    },
    'handlers': {
        'console': {
            'formatter': 'console',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'formatter': 'json',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'bob.log',
            'mode': 'a',
            'delay': '1',
            'maxBytes': 1000000,
            'backupCount': 3,
        },
    },
    'loggers': {
        'bob': {
            'level': 'DEBUG',
            'handlers': [
                'console',
                'file',
            ],
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': [
            'console',
            'file',
        ],
    }
}
