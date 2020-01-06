"""
    Хлебные крошки.

    Установка:
        settings.py:
            MIDDLEWARE_CLASSES = (
                ...
                'breadcrumbs.middleware.BreadcrumbsMiddleware',
                ...
            )

            INSTALLED_APPS = (
                ...
                'breadcrumbs',
                ...
            )

    Пример:
        views.py:
            def my_page(request):
                ...
                request.breadcrumbs.add('Home', 'http://ya.ru')
                request.breadcrumbs.add('Company', '/company/')
                request.breadcrumbs.add('My Page', 'company:page', page_id=1, classes="active")
                ...

        template.html:
            {% load breadcrumbs %}

            ...

            {% breadcrumbs %}
            или
            {% breadcrumbs template='breadcrumbs/custom.html' %}
"""
