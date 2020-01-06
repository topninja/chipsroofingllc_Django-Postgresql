from django.conf import settings


MULTILANGUAGE_SITES = settings.MULTILANGUAGE_SITES

# если авторедирект на текущий сайт приводит на страницу,
# которой нет - редиректим на страницу MULTILANGUAGE_FALLBACK_URL
MULTILANGUAGE_FALLBACK_URL = getattr(settings, 'MULTILANGUAGE_FALLBACK_URL', 'index')

# имя куки, хранящей флаг того, что редиректить автоматически с данного сайта не нужно
MULTILANGUAGE_COOKIE_KEY = getattr(settings, 'MULTILANGUAGE_COOKIE_KEY', 'no_redirect')

# Имя GET-параметра, запрещающего авторедирект
MULTILANGUAGE_GET_PARAM = 'no_redirect'

# Строки в User-Agent, для которых запещён редирект
ROBOTS_UA = tuple(map(str.lower, (
    'Googlebot',
    'Google Page Speed',
    'Mail.RU_Bot',
    'YandexBot',
    'YandexImage',
    'YandexMetrika',
    'Applebot',
    'facebookexternalhit',
    'DuckDuckBot',
    'SkypeUriPreview',
    'Pinterest',
    'Twitterbot',
    'Slackbot',
    'vkShare',
    'Yahoo',
    'W3C_Validator',
)))
