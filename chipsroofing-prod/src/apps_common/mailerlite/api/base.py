import re
import requests
from libs.associative_request import associative
from .. import conf

__all__ = ['SubscribeAPIError', 'request']
re_filter = re.compile('([^\[]+)\[([^\]]+)\]')


class SubscribeAPIError(Exception):
    @property
    def code(self):
        return self.args[0]

    @property
    def message(self):
        return self.args[1]


def parse_filters(filters):
    """
        Форматирование фильтров.
        Допустимые форматы:
            1) {
                'date_created[$gte]': '2017-09-21',
            }
    """
    if not filters:
        return {}

    result = {}
    for key, value in filters.items():
        match = re_filter.match(key)
        if match:
            result.setdefault(match.group(1), {}).setdefault(match.group(2), value)
    return result


def request(api_method, method='GET', params=None, data=None, version=2):
    """ Запрос к API """
    url = 'https://api.mailerlite.com/api/v%d/%s' % (version, api_method)
    headers = {
        'X-MailerLite-ApiKey': conf.APIKEY,
    }
    response = requests.request(method, url,
        headers=headers,
        params=associative(params),
        data=associative(data),
        timeout=(5, 10),
    )

    try:
        data = response.json()
    except ValueError:
        return None

    if 'error' in data:
        raise SubscribeAPIError(data['error']['code'], data['error']['message'])

    return data
