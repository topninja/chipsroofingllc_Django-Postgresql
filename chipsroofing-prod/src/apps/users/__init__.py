"""
    Модуль пользователей.

    Содержит каркас обработки стандартных событий (авторизация, регистрация и т.п.).

    Модель пользователя - кастомная: добавлен аватар.

    Установка:
        urls.py:
            ...
            url(r'^users/', include('users.urls', namespace='users')),

        app.py:
            def ready(self):
                from django.shortcuts import resolve_url
                from django.templatetags.static import static
                from libs.js_storage import JS_STORAGE

                JS_STORAGE.update({
                    'ajax_login': resolve_url('users:ajax_login'),
                    'ajax_logout': resolve_url('users:ajax_logout'),
                    'ajax_register': resolve_url('users:ajax_register'),
                    'ajax_reset': resolve_url('users:ajax_reset'),
                    'ajax_reset_confirm': resolve_url('users:ajax_reset_confirm'),
                    'plupload_moxie_swf': static('common/js/plupload/Moxie.swf'),
                    'plupload_moxie_xap': static('common/js/plupload/Moxie.xap'),
                })

"""

default_app_config = 'users.apps.Config'
