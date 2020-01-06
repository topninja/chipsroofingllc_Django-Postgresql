import os
import re
import sys
from django.utils.translation import ugettext_lazy as _
from .pipeline import PIPELINE

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps_common'))

SECRET_KEY = '+1xmf1u00*m*3g@@w)o#sy_*_b!=^61blmldss6x#0%##a4rny'

DEBUG = False

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)

TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_cron',
    'mptt',
    'pipeline',
    'solo',
    'suit_ckeditor',

    # Apps
    'config',
    'contacts',
    'services',
    'blog',
    'main',
    'examples',
    'about',
    'testimonials',
    'users',
    'faq',
    'blocks',
    'std_page',

    # Apps common
    'admin_ctr',
    'admin_honeypot',
    'admin_log',
    'attachable_blocks',
    'breadcrumbs',
    'backups',
    'ckeditor',
    'footer',
    'gallery',
    'google_maps',
    'header',
    'menu',
    'paginator',
    'placeholder',
    'seo',
    'social_networks',
    'rating',

    # Libs
    'libs.autocomplete',
    'libs.away',
    'libs.color_field',
    'libs.file_field',
    'libs.form_helper',
    'libs.js_storage',
    'libs.management',
    'libs.pipeline',
    'libs.sprite_image',
    'libs.stdimage',
    'libs.templatetags',
    'libs.variation_field',
)

# Suit
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Chips Roofing & Exteriors, LLC',

    # search
    'SEARCH_URL': '',

    # menu
    'MENU': (
        {
            'app': 'main',
            'icon': 'icon-file',
            'models': (
                'MainPageConfig',
                'ExamplesPageConfig',
            )
        },
        '-',
        {
            'app': 'services',
            'icon': 'icon-file',
            'models': (
                'ServicesConfig',
                'Service',
            )
        },
        {
            'app': 'faq',
            'icon': 'icon-file',
            'models': (
                'FaqConfig',
                'Faq',
            )
        },
        {
            'app': 'blog',
            'icon': 'icon-file',
            'models': (
                'BlogConfig',
                'BlogPost',
                'Tag',
            )
        },
        '-',
        {
            'app': 'examples',
            'icon': 'icon-file',
            'models': (
                'ExamplesPageConfig',
            )
        },
        {
            'app': 'testimonials',
            'icon': 'icon-file',
            'models': (
                'TestimonialsPageConfig',
                'Testimonials'
            )
        },
        '-',
        {
            'app': 'contacts',
            'icon': 'icon-file',
            'models': (
                'ContactsConfig',
                'Address',
                'Message',
            )
        },
        {
            'app': 'about',
            'icon': 'icon-file',
            'models': (
                'AboutPageConfig',
            )
        },
        '-',
        {
            'app': 'config',
            'icon': 'icon-lock',
            'models': (
                'Config',
            )
        },
        {
            'app': 'social_networks',
            'icon': 'icon-lock',
            'models': (
                'FeedPost',
                'SocialLinks',
                'SocialConfig',
            )
        },
        '-',
        {
            'icon': 'icon-lock',
            'label': 'Authentication and Authorization',
            'permissions': 'users.change_customuser',
            'models': (
                'auth.Group',
                'users.CustomUser',
            )
        },
        {
            'app': 'backups',
            'icon': 'icon-hdd',
            'permissions': 'users.admin_menu',
        },
        {
            'app': 'django_cron',
            'icon': 'icon-hdd',
            'permissions': 'users.admin_menu',
        },
        {
            'app': 'admin',
            'icon': 'icon-list-alt',
            'label': _('History'),
            'permissions': 'users.admin_menu',
        },
        {
            'app': 'sites',
            'permissions': 'users.admin_menu',
        },
        {
            'app': 'seo',
            'icon': 'icon-tasks',
            'permissions': 'users.admin_menu',
            'models': (
                'SeoConfig',
                'Redirect',
                'Counter',
                'Robots',
            ),
        },
    ),
}

# Pipeline
SASS_INCLUDE_DIR = BASE_DIR + '/static/scss/'
PIPELINE['SASS_BINARY'] = '/usr/bin/env sassc --load-path ' + SASS_INCLUDE_DIR

MIDDLEWARE_CLASSES = (
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'libs.cache.middleware.SCCMiddleware',
    'libs.js_storage.middleware.JSStorageMiddleware',
    'libs.middleware.xss.XSSProtectionMiddleware',
    'libs.middleware.utm.UTMMiddleware',
    'menu.middleware.MenuMiddleware',
    'seo.middleware.RedirectMiddleware',
    'breadcrumbs.middleware.BreadcrumbsMiddleware',
)

ALLOWED_HOSTS = ()

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

# Sites and users
SITE_ID = 1
ANONYMOUS_USER_ID = -1
AUTH_USER_MODEL = 'users.CustomUser'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'index'
LOGIN_REDIRECT_URL = 'index'
RESET_PASSWORD_REDIRECT_URL = 'index'
LOGOUT_URL = 'index'

# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'noreply@mail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'noreply@mail.com'
EMAIL_SUBJECT_PREFIX = '[%s] ' % (SUIT_CONFIG['ADMIN_NAME'], )

# ==================================================================
# ==================== APPS SETTINGS ===============================
# ==================================================================

# Admin Dump
BACKUP_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'backup'))

# Директория для robots.txt и других открытых файлов
PUBLIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'public'))

# Django solo caching
SOLO_CACHE = 'default'
SOLO_CACHE_TIMEOUT = 10 * 60

# Smart Cache-Control
SCC_IGNORE_URLS = [
    r'/admin/',
    r'/dladmin/',
]

# Формат валют (RUB / USD / EUR / GBP)
# Для включения зависимости от языка сайта - задать None или удалить
VALUTE_FORMAT = None

# Django Cron
CRON_CLASSES = [

]

# ==================================================================
# ==================== END APPS SETTINGS ===========================
# ==================================================================

# Домен для куки сессий (".example.com")
SESSION_COOKIE_DOMAIN = None
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 30 * 24 * 3600

# Домен для куки CSRF (".example.com")
CSRF_COOKIE_DOMAIN = None

# Список скомпилированных регулярных выражений
# запретных юзер-агентов
DISALLOWED_USER_AGENTS = ()

# Получатели писем о ошибках при DEBUG = False
ADMINS = (
)

# Получатели писем о битых ссылках при DEBUG=False
# Требуется подключить django.middleware.common.BrokenLinkEmailsMiddleware
MANAGERS = (
)

# Список скомпилированных регулярных выражений адресов страниц,
# сообщения о 404 на которых не должны отправляться на почту (MANAGERS)
IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)

# DB
DATABASES = {}

# Cache
CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379:0",
        "KEY_PREFIX": LANGUAGE_CODE + SECRET_KEY,
        "OPTIONS": {
            "CLIENT_CLASS": 'django_redis.client.DefaultClient',
            "PASSWORD": "",
        }
    }
}

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            os.path.join(BASE_DIR, 'templates'),
        ),
        'OPTIONS': {
            'context_processors': (
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'contacts.context_processors.google_recaptcha_public_key',
                'social_networks.context_processors.google_apikey',
                'libs.context_processors.domain',
            ),
            'loaders': (
                ('django.template.loaders.cached.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                )),
            ),
        }
    },
]

# Locale
LOCALE_PATHS = (
    'locale',
)

# Datetime formats
FORMAT_MODULE_PATH = [
    'project.formats',
]

# Media
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'media'))
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

CAPTCHA_AJAX = True

GOOGLE_RECAPTCHA_SECRET_KEY = '6LehSJsUAAAAAH3dB4Ad_22_Hr_BVsRnOMo638zT'
GOOGLE_RECAPTCHA_PUBLIC_KEY = '6LehSJsUAAAAAAcQwxzlPwNwbTccsJWFPQO3YWOd'