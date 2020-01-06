"""
    Модуль оплаты через Robokassa.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'robokassa',
                ...
            )

            ROBOKASSA_LOGIN = 'stroisad'
            ROBOKASSA_PASSWORD1 = 'qX11LDagwPqmC1ofI45n'
            ROBOKASSA_PASSWORD2 = 's6mTLawO0Ehc06Cc6rLT'
            ROBOKASSA_TEST_MODE = True

            SUIT_CONFIG = {
                ...
                {
                    'app': 'robokassa',
                    'icon': 'icon-shopping-cart',
                    'models': (
                        'log',
                    )
                },
                ...
            }

        urls.py:
            ...
            url(r'^robokassa/', include('robokassa.urls', namespace='robokassa')),
            ...

    Настройки (settings.py):
        # Логин магазина
        ROBOKASSA_LOGIN = 'super_shop'

        # Первый пароль магазина
        ROBOKASSA_PASSWORD1 = 'a123b5c6h'

        # Второй пароль магазина
        ROBOKASSA_PASSWORD2 = 'nkvo6s8bv'

        # === Не обязательные ===

        # Используется ли метод POST для ResultURL
        ROBOKASSA_USE_POST = True

        # Тестовый режим магазина
        ROBOKASSA_TEST_MODE = False

        # Дополнительные данные уведомлений
        ROBOKASSA_EXTRA_PARAMS = ['shp_param1', 'shp_param2']

    Пример:
        views.py:
            from robokassa.forms import PaymentForm
            from robokassa.signals import robokassa_success

            ...
            form = PaymentForm(initial={
                'invoice': 1,
                'amount': '12.50',
                'description': 'Золотое кольцо',
            })

            # можно сразу перенаправить
            return redirect(form.get_redirect_url())
            ...

            @receiver(robokassa_success)
            def payment_success(sender, **kwargs):
                invoice = kwargs['invoice']
                request = kwargs['request']

        template.html:
            <form action="{{ form.target }}" method="post">
              {{ form.as_p }}
              <button type="submit">Pay</button>
            </form>
"""

default_app_config = 'robokassa.apps.Config'
