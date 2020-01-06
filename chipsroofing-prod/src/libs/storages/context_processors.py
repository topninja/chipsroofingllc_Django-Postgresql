from .utils import MEDIA_URLS


def media_urls(request):
    return {
        'MEDIA_URLS': MEDIA_URLS,
    }
