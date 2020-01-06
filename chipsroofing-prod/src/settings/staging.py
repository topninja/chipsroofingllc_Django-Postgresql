from settings.common import *

SUBDOMAIN = 'chipsroofing'
DOMAIN = '.%s.dev.directlinedev.com' % SUBDOMAIN
VZ_DIRECTORY = '/home/webapp/domains/%s.dev.directlinedev.com' % SUBDOMAIN

SESSION_COOKIE_DOMAIN = DOMAIN
CSRF_COOKIE_DOMAIN = DOMAIN

# Метка %SECRET_KEY% при развёртывании заменяется на нужный секретный ключ
SECRET_KEY = '%SECRET_KEY%'

ALLOWED_HOSTS = (
    DOMAIN,
)

# настройки статики
STATIC_ROOT = os.path.join(VZ_DIRECTORY, 'static')
MEDIA_ROOT = os.path.join(VZ_DIRECTORY, 'media')
BACKUP_ROOT = os.path.join(VZ_DIRECTORY, 'backup')
PUBLIC_DIR = os.path.join(VZ_DIRECTORY, 'public')

DATABASES.update({
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': SUBDOMAIN,
        'USER': 'webapp',
        'PASSWORD': '%DBPASSWORD%',
        'HOST': 'localhost',
        'CONN_MAX_AGE': 60,
    }
})

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s]: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(VZ_DIRECTORY, 'django_errors.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['file'],
            'level': 'ERROR',
        }
    },
}

