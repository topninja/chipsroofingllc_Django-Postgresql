"""
    Кастомный сервер для разработки.

    Установка:
        INSTALLED_APPS = (
            'devserver',
            ...
        )

        MIDDLEWARE_CLASSES = (
            ...
            'devserver.middleware.DevServerMiddleware',
        )

    Настройки:
        DEVSERVER_MODULES = (...)
        DEVSERVER_IGNORED_PREFIXES = (
            settings.STATIC_URL,
            settings.MEDIA_URL,
            '/favicon',
        )


    Профилирование функций:
        from devserver.profiler import profile

        @profile(show_sql=True)
        def get(self, request, post_id):
            ...

    Профилирование участков кода:
        from devserver.profiler import Profile

        with Profile('FetchEntity', show_sql=True):
            e = Entity.objects.get(pk=1)

        with Profile('LogToFile', stdout='/tmp/log.txt', show_sql=True):
            e = Entity.objects.get(pk=1)
"""
