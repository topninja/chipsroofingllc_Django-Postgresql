from .dev_common import *

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

PIPELINE['PIPELINE_ENABLED'] = False

DOMAIN = '127.0.0.1'
SESSION_COOKIE_DOMAIN = DOMAIN
CSRF_COOKIE_DOMAIN = DOMAIN
ALLOWED_HOSTS = (
    DOMAIN,
    'localhost',
    '127.0.0.1',
)

