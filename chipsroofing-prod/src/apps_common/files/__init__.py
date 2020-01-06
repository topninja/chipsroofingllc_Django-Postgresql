"""
    Модуль файлов на страницу.

    Зависит от:
        libs.storages
        libs.download

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'files',
                ...
            )

        urls.py:
            ...
            url(r'^files/', include('files.urls', namespace='files')),

    Пример:
        # models.py:
            from django.contrib.contenttypes import generic

            class Module(models.Model):
                files = generic.GenericRelation(PageFile, limit_choices_to={
                    'set_name': 'module-files'
                })

        # admin.py:
            from files.admin import PageFileInline

            class ModuleFileInline(PageFileInline):
                set_name = 'module-files'
                suit_classes = 'suit-tab suit-tab-general'
"""

default_app_config = 'files.apps.Config'
