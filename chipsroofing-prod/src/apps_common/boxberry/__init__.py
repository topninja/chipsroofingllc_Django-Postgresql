"""
    API сервиса BOXBERRY.

    http://boxberry.ru/upload/iblock/f2c/Интеграция%20модуля%20выбора%20пункта%20выдачи.pdf
    http://boxberry.ru/upload/iblock/50d/web-сервисы%20Boxberry.pdf

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'boxberry',
                ...
            )

            # тестовый режим
            BOXBERRY_TEST = False

            # ключ интеграции для виджета
            BOXBERRY_KEY = 'gfgiLAIqtr8qn4kciPkUmw=='

            # токен тестового режима
            BOXBERRY_API_TEST_TOKEN = '31705.rvpqcbfd'

            # токен реального режима
            BOXBERRY_API_TOKEN = '12345.abcdefgh'

    Пример:
        ...
"""

default_app_config = 'boxberry.apps.Config'
