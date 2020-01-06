"""
    СЕО-модуль.

    Зависит от:
        libs.storages

    1) Позволяет указывать значения title, keywords, desription
    2) Указание <link rel="canonical">
    3) Указание некоторых OpenGraph-метаданных.
    4) Управление содержимым robots.txt
    5) Добавление JS-счётчиков

    Необязательные настройки:
        # Если не пустая строка - она будет объединять части <title> страницы.
        # Если пустая строка - будет выведен только первый элемент дэка
        SEO_TITLE_JOIN_WITH = ' | '

    Подключение к модели:
        page/admin.py:
            ...
            class PageAdmin(SeoModelAdminMixin, admin.ModelAdmin):
                ...

    Установка параметров по умолчанию:
        views.py:
            from seo.seo import Seo

            # Простейшая установка SEO-данных из объекта SeoData, привязанного к entity:
                seo = Seo()
                seo.set_data(entity, defaults={
                    'title': entity.title,
                    'og_title': entity.title,
                })
                seo.save(request)

            # Установка цепочки заголовков:
                seo = Seo()
                seo.set_title(shop, default=shop.title)
                seo.set_title(category, default=category.title)
                seo.set_data(product, defaults={
                    'title': product.title,
                })
                seo.save(request)

    Счетчики:
        {% load seo %}

        <head>
            <title>{{ request.seo.title }}</title>
            {% include 'seo/metatags.html' %}
            {% seo_counters 'head' %}
        </head>
        <body>
            {% seo_counters 'body_top' %}
            ...
            {% seo_counters 'body_bottom' %}
        </body>
"""

default_app_config = 'seo.apps.Config'
