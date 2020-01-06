from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import resolve_url
from . import options


def get_referer_url(request):
    """
        Возвращает относительный путь REFERER, если он с текущего сайта.
        Иначе, возвращает MULTILANGUAGE_FALLBACK_URL
    """
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return resolve_url(options.MULTILANGUAGE_FALLBACK_URL)

    site = get_current_site(request)
    url_parts = list(urlparse(referer))
    if url_parts[1] != site.domain:
        return resolve_url(options.MULTILANGUAGE_FALLBACK_URL)

    url_parts[0] = ''
    url_parts[1] = ''
    return urlunparse(url_parts)


def noredirect_url(url, forced_path=None):
    """
        Добавление к урлу параметра, запрещающего авторедирект
    """
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))

    if forced_path:
        forced_path_parts = list(urlparse(forced_path))
        url_parts[2] = forced_path_parts[2]
        forced_path_query = dict(parse_qsl(forced_path_parts[4]))
        query.update(forced_path_query)

    query.update({
        options.MULTILANGUAGE_GET_PARAM: 1
    })
    url_parts[4] = urlencode(query)

    return urlunparse(url_parts)
