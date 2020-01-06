from django.conf import settings


MEDIA_URLS = tuple(
    host if host.endswith('/') else host + '/'
    for host in getattr(settings, 'MEDIA_URLS', ())
)
