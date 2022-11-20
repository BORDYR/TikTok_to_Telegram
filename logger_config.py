import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },

    'handlers': {
        'File_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default_formatter',
            'filename': 'logs/TTtoTG-saver.log',
            'maxBytes': 1_000_000,
            'backupCount': 1

        },
    },

    'loggers': {
        'TTtoTG_logger': {
            'handlers': ['File_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}