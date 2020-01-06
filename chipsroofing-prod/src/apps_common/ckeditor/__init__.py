"""
    CKEditorField - стандартное поле ckeditor.
    CKEditorUploadField - поле ckeditor с возможностью закачки файлов.

    Зависит от:
        libs.storages
        libs.stdimage
        libs.upload

    Можно поставить на крон удаление картинок, которые не привязаны к сущности:
        pm clean_pagephotos

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'suit_ckeditor',
                'ckeditor',
                ...
            )

        urls.py:
            ...
            url(r'^dladmin/ckeditor/', include('ckeditor.admin_urls', namespace='admin_ckeditor')),
            url(r'^ckeditor/', include('ckeditor.urls', namespace='ckeditor')),
            ...


        Пример использования:
            models.py:
                from ckeditor.fields import CKEditorUploadField

                class MyModel(models.Model):
                    ...
                    text = CKEditorUploadField(_('text'))
                    ...

"""

default_app_config = 'ckeditor.apps.Config'
