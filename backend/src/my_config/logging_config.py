LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': 'app.log',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'app': {  # specific logger for your Flask app
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False  # Prevent messages from propagating to root if handled here
        },
        'controllers.users': {  # specific logger for your users controller
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
