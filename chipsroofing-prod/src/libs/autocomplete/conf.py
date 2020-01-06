from django.conf import settings

AUTOCOMPLETE_CACHE_BACKEND = getattr(settings, 'AUTOCOMPLETE_CACHE_BACKEND', 'default')
CACHE_TIMEOUT = 2 * 3600
