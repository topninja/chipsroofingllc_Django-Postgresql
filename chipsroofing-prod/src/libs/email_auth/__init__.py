"""
    Для авторизации по паре email-пароль.

    Установка:
        # settings.py:
            AUTHENTICATION_BACKENDS = (
                'django.contrib.auth.backends.ModelBackend',
                'libs.email_auth.backends.EmailModelBackend',
            )
"""
