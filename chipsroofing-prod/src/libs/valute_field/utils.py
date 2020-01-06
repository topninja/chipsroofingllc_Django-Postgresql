import re
from django.conf import settings
from django.utils.translation import get_language
from django.core.exceptions import ImproperlyConfigured
from . import conf

re_price = re.compile(r'^(-?\d+)(\d{3})')


def get_formatter(language=None):
    if conf.VALUTE_FORMAT:
        valute_format = conf.VALUTE_FORMAT
    else:
        language = language or get_language() or settings.LANGUAGE_CODE
        for langs, valute_format in conf.VALUTE_FORMAT_BY_LANG.items():
            if language in langs:
                break
        else:
            raise ImproperlyConfigured("Valute format not found for language '%s'" % language)

    return conf.VALUTE_FORMATS[valute_format.upper()]


def split_price(value, join=' '):
    """ Разделение цены по разрядам """
    new = re_price.sub('\\1{}\\2'.format(join), value)
    if value == new:
        return new
    else:
        return split_price(new, join)
