LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) - {name} - {module} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '({levelname}) - {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'handlers': {
        'debug': {
            'class': 'logging.FileHandler',
            'filename': 'logger/1_debug.log',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'info': {
            'class': 'logging.FileHandler',
            'filename': 'logger/2_info.log',
            'formatter': 'verbose',
            'level': 'INFO',
            'filters': ['require_debug_false'],
        },
        'warning': {
            'class': 'logging.FileHandler',
            'filename': 'logger/3_warning.log',
            'formatter': 'verbose',
            'level': 'WARNING',
            'filters': ['require_debug_false'],
        },
        'error': {
            'class': 'logging.FileHandler',
            'filename': 'logger/4_error.log',
            'formatter': 'verbose',
            'level': 'ERROR',
            'filters': ['require_debug_false'],
        },
        'critical': {
            'class': 'logging.FileHandler',
            'filename': 'logger/5_critical.log',
            'formatter': 'verbose',
            'level': 'CRITICAL',
            'filters': ['require_debug_false'],
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
    },
    'loggers': {
        '': {
            'handlers': [
                'debug', 
                'info', 
                'warning', 
                'error', 
                'critical', 
                'mail_admins',
            ],
        },
    },
}
