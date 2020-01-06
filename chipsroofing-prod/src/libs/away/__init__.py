"""
    Модуль замены внешних ссылок на единую точку редиректов.

    Установка:
        urls.py:
            ...
            url(r'^away/$', 'libs.away.views.away', name='away'),
            ...

    Использование:
        template.html:
            {% load away %}
            ...
            {% away text|striptags|linebreaksbr|urlize %}
"""
