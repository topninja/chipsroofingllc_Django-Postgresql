"""
    Поле для хранения цены в формате decimal.

    Для вывода валют в email-письмах следует использовать формат вывода alternative,
    т.к. в шрифтах писем нет UTF-символа рубля.

    Необязательные настройки:
        # Принудительная установка формата валют (независимо от языка).
        # Доступные форматы: RUB, USD, EUR, GBP
        VALUTE_FORMAT = 'EUR'

        # Свои форматы валют (объединяется с настройками по умолчанию)
        VALUTE_FORMATS = {
            'USD': {
                'trail': True,
            }
        }

        # Соответствия формата валюты языку сайта (когда VALUTE_FORMAT == None)
        VALUTE_FORMAT_BY_LANG = {
            ('en', 'fr'): 'USD',
            ('ru',): 'RUB',
        }

    Пример:
        price = ValuteField(_('цена'))

        ru:
            $ v = Valute('1234.00')
            $ print(v)
            1 234 ₽

            $ print(v.utf)
            1 234 ₽

            $ print(v.alternative)
            1 234 руб.

            $ print(v.simple)
            1 234.00

            $ print(v.trailed)
            1 234

    Управление округлением:
        $ v = Valute('100')
        $ print(v / 3)
        $33.34

        $ with v.rounding(floor=True):
              print(v / 3)
        $33.33
"""
