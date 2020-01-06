from settings.common import *

SECRET_KEY = '%(t39$j^tu!axm00nq5=ls&*j&f^pp5fwzqz$(0f(u!!zs3b1%'

PIPELINE['SASS_BINARY'] = '/usr/bin/env /usr/local/bin/sassc --load-path ' + SASS_INCLUDE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
