from django.conf import settings


# Форматы вывода валют ValuteField в зависимости от языка
#    decimal_places     - кол-во чисел после запятой
#    decimal_mark       - разделитель целого и частного
#    thousands          - разделитель тысячных разрядов
#    trail              - не выводить дробную часть, если в ней только нули
#    utf_format         - формат с использованием UTF-символов
#    alternative_format - формат без использования UTF-символов
#    widget_attrs       - дополнительные параметры виждета
VALUTE_FORMATS = {
    'RUB': {
        'decimal_places': 2,
        'decimal_mark': '.',
        'thousands': ' ',
        'trail': True,

        'utf_format': '{}\u20bd',
        'alternative_format': '{} руб.',
        'widget_attrs': {
            'append': 'руб.',
        },
    },
    'USD': {
        'decimal_places': 2,
        'decimal_mark': '.',
        'thousands': ',',
        'trail': True,

        'utf_format': '${}',
        'alternative_format': '${}',
        'widget_attrs': {
            'prepend': '$',
        },
    },
    'EUR': {
        'decimal_places': 2,
        'decimal_mark': ',',
        'thousands': '',
        'trail': False,
        'utf_format': '{}€',
        'alternative_format': '{}€',
        'widget_attrs': {
            'append': '€',
        },
    },
    'GBP': {
        'decimal_places': 2,
        'decimal_mark': '.',
        'thousands': ',',
        'trail': False,
        'utf_format': '£{}',
        'alternative_format': '£{}',
        'widget_attrs': {
            'prepend': '£',
        },
    },
}

# Форматы валют (по умолчанию + пользовательские)
for key, format_dict in getattr(settings, 'VALUTE_FORMATS', {}).items():
    key = key.upper()
    if key in VALUTE_FORMATS:
        VALUTE_FORMATS[key].update(format_dict)
    else:
        VALUTE_FORMATS[key] = format_dict

# Единый принудительный формат валют на сайте
VALUTE_FORMAT = getattr(settings, 'VALUTE_FORMAT', None)

# Соответствия форматов валют языкам сайта (если VALUTE_FORMAT == None)
VALUTE_FORMAT_BY_LANG = getattr(settings, 'VALUTE_FORMAT_BY_LANG', {
    ('en',): 'USD',
    ('ru',): 'RUB',
})
