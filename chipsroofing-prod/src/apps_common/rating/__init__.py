"""
    Модуль голосования для составления реётинга сайта (для schema.org).

    Зависит от:
        libs.cookies
        libs.range_field

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'rating',
                ...
            )

        urls.py:
            ...
            url(r'^rating/', include('rating.urls', namespace='rating')),
            ...

"""

default_app_config = 'rating.apps.Config'
