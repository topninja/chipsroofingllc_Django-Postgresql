"""
    Хранилище JS-переменных для вывода в шаблон.
    Интерфейс идентичен интерфейсу словаря.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.js_storage',
                ...
            )

            MIDDLEWARE_CLASSES = (
                ...
                'libs.js_storage.middleware.JSStorageMiddleware',
                ...
            )

    Пример:
        # views.py:
            def my_page(request):
                ...
                request.js_storage['var1'] = 5
                request.js_storage.update(x=1, y='2')
                ...

        # Можно объявлять переменные для всего сайта:
        # apps.py:
            class Config(AppConfig):
                name = 'users'
                verbose_name = "Пользователи"

                def ready(self):
                    from django.shortcuts import resolve_url
                    from libs.js_storage import JS_STORAGE

                    JS_STORAGE.update({
                        'ajax_register': resolve_url('users:ajax_register')
                    })

    В JavaScript переменные доступны как члены глобального объекта js_storage:
        $.ajax({
            url: js_storage.var1,
        })


    В шаблоне необходимо добавить тэг js_storage_out:
        {% load js_storage %}
        ...
        {% js_storage_out %}
"""

JS_STORAGE = {}
