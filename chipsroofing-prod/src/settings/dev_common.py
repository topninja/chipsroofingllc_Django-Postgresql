from settings.common import *

DOMAIN = '.local.com'
SESSION_COOKIE_DOMAIN = DOMAIN
CSRF_COOKIE_DOMAIN = DOMAIN
ALLOWED_HOSTS = (
    DOMAIN,
    'localhost',
    '127.0.0.1',
)

DEBUG = True

DATABASES.update({
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'project',
        'USER': 'project',
        'PASSWORD': 'password',
        'HOST': 'localhost',
    }
})

# Нарезка в два потока (на продакшене для этого памяти не хватит)
VARIATION_THREADS = 2

# Отключение компрессии SASS (иначе теряется наглядность кода)
PIPELINE['SASS_ARGUMENTS'] = '-t nested'

STATICFILES_FINDERS += (
    'libs.pipeline.debug_finder.PipelineFinder',
)


INSTALLED_APPS = (
    'devserver',
) + INSTALLED_APPS

MIDDLEWARE_CLASSES += 'devserver.middleware.DevServerMiddleware',

# Вывод ошибок в консоль
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'requests': {
            'handlers': ['null'],
            'propagate': False,
        },
        'sql': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    },
}
