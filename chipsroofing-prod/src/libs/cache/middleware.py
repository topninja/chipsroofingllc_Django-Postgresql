import re
import logging
from django.conf import settings
from django.utils.cache import patch_vary_headers

logger = logging.getLogger(__name__)
ENABLED = getattr(settings, 'SCC_ENABLED', not settings.DEBUG)
MAX_AGE_PUBLIC = getattr(settings, 'SCC_MAX_AGE_PUBLIC', 24 * 3600)
MAX_AGE_PRIVATE = getattr(settings, 'SCC_MAX_AGE_PRIVATE', 0)
VARY_ON = getattr(settings, 'SCC_VARY_ON', ('Cookie', ))

IGNORE_URLS = []
for url_settings in getattr(settings, 'SCC_IGNORE_URLS', []):
    IGNORE_URLS.append(re.compile(url_settings))

CUSTOM_RULES = []
for url_settings in getattr(settings, 'SCC_CUSTOM_RULES', []):
    CUSTOM_RULES.append((
        re.compile(url_settings[0]),
        url_settings[1],
        url_settings[2],
    ))


class SCCMiddleware:
    @staticmethod
    def process_response(request, response):
        if not ENABLED:
            # Удаление кэширующих заголовков
            if 'last-modified' in response:
                del response['last-modified']
            if 'etag' in response:
                del response['etag']
            return response

        # Если не указан content-type - выходим
        if 'content-type' not in response:
            return response

        # Если не HTML-страница - выходим
        if 'text/html' not in response['content-type']:
            return response

        # Если нет юзера - выходим
        if not hasattr(request, 'user'):
            return response

        # Игнорируемые для кэширования адреса
        for url in IGNORE_URLS:
            if url.match(request.path_info):
                return response

        # Если заголовок уже установлен - не меняем его
        if 'cache-control' not in response:
            # пользовательские правила
            exact_rules = []
            regex_rules = []
            for rule in CUSTOM_RULES:
                if rule[0].match(request.path_info):
                    pattern = rule[0].pattern.lstrip('^')
                    if pattern.endswith('$'):
                        exact_rules.append({
                            'rule': rule,
                            'length': len(pattern) - 1,
                        })
                    else:
                        regex_rules.append({
                            'rule': rule,
                            'length': len(pattern),
                        })

            if exact_rules:
                rule = sorted(exact_rules, key=lambda x: x['length'], reverse=True)[0]['rule']
                response['Cache-Control'] = '{}, must-revalidate, max-age={}'.format(*rule[1:])
            elif regex_rules:
                rule = sorted(regex_rules, key=lambda x: x['length'], reverse=True)[0]['rule']
                response['Cache-Control'] = '{}, must-revalidate, max-age={}'.format(*rule[1:])
            else:
                if request.user.is_authenticated():
                    response['Cache-Control'] = 'private, must-revalidate, max-age={}'.format(
                        MAX_AGE_PRIVATE
                    )
                else:
                    response['Cache-Control'] = 'public, must-revalidate, max-age={}'.format(
                        MAX_AGE_PUBLIC
                    )

        # Кэш должен различаться для разных кук
        patch_vary_headers(response, VARY_ON)

        return response
