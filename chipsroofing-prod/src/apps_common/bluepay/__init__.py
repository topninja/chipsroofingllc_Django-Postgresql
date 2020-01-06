"""
    Модуль оплаты через BluePay.

    Для прода нужно заказывать уведомления:
        https://www.bluepay.com/developers/api-documentation/python/get-data/trans-notify/

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'bluepay',
                ...
            )

            BLUEPAY_MERCHANT_NAME = 'Mega Shop'
            BLUEPAY_ACCOUNT_ID = 100478206419
            BLUEPAY_USER_ID = 100478206420
            BLUEPAY_SECRET_KEY = '4FBGCHCRE/33NRVRMBGIKOGET6DLQ0ZL'
            BLUEPAY_TEST_MODE = True

            SUIT_CONFIG = {
                ...
                {
                    'app': 'bluepay',
                    'icon': 'icon-shopping-cart',
                    'models': (
                        'log',
                    )
                },
                ...
            }

        urls.py:
            ...
            url(r'^bluepay/', include('bluepay.urls', namespace='bluepay')),
            ...

    Настройки (settings.py):
        # Название магазина
        BLUEPAY_MERCHANT_NAME = 'Mega Shop'

        # Данные аккаунта
        BLUEPAY_ACCOUNT_ID = 100478206419
        BLUEPAY_USER_ID = 100478206420
        BLUEPAY_SECRET_KEY = '4FBGCHCRE/33NRVRMBGIKOGET6DLQ0ZL'

        # Адрес страницы, куда перенаправит пользователя
        # после успешной оплаты
        BLUEPAY_SUCCESS_URL = 'shop:index'

        # Адрес страницы, куда перенаправит пользователя
        # после неудачной оплаты
        BLUEPAY_FAIL_URL = 'shop:index'

    Пример:
        views.py:
            from bluepay.forms import PaymentForm
            from bluepay.signals import bluepay_success, bluepay_error

            ...
            form = PaymentForm(request, initial={
                'invoice': 1,
                'amount': '11.00',
            })

            # можно сразу перенаправить
            return redirect(form.get_redirect_url())
            ...


            @receiver(bluepay_success)
            def payment_success(sender, **kwargs):
                invoice = kwargs['invoice']
                request = kwargs['request']

            @receiver(bluepay_error)
            def payment_error(sender, **kwargs):
                invoice = kwargs['invoice']
                request = kwargs['request']
                code = kwargs['code']
                reason = kwargs['reason']

        template.html:
            <form action="{{ form.target }}" method="post">
              {{ form }}
              <button type="submit">Pay</button>
            </form>

"""

default_app_config = 'bluepay.apps.Config'
