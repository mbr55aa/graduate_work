from .base import *

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s: %(message)s [in %(pathname)s:%(lineno)d]'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'default': {
            'format': LOG_FORMAT,
        },
    },
    'handlers': {
        'debug-console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['debug-console'],
            'propagate': False,
        }
    },
}
