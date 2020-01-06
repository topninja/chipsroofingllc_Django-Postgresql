"""
    Модуль оплаты через Gotobilling.

    http://www.gotobilling.com/wiki/index.php?title=One_Click
    http://www.gotobilling.com/wiki/index.php?title=Advanced_Integration_Method

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'gotobilling',
                ...
            )

            GOTOBILLING_MID = 122879
            GOTOBILLING_HASH = 'myShop123'
            GOTOBILLING_SUCCESS_URL = 'shop:index'
            GOTOBILLING_FAIL_URL = 'shop:index'

            SUIT_CONFIG = {
                ...
                {
                    'app': 'gotobilling',
                    'icon': 'icon-shopping-cart',
                    'models': (
                        'log',
                    )
                },
                ...
            }

        urls.py:
            ...
            url(r'^gotobilling/', include('gotobilling.urls', namespace='gotobilling')),
            ...

    Настройки (settings.py):
        # ID магазина
        GOTOBILLING_MID = 122879

        # Gateway Hash
        GOTOBILLING_HASH = 'myShop123'

        # Адрес страницы, куда перенаправит пользователя
        # после успешной оплаты
        GOTOBILLING_SUCCESS_URL = 'shop:index'

        # Адрес страницы, куда перенаправит пользователя
        # после неудачной оплаты
        GOTOBILLING_FAIL_URL = 'shop:index'

    Пример:
        views.py:
            from gotobilling.forms import PaymentForm
            from gotobilling.signals import gotobilling_success, gotobilling_error

            ...
            form = PaymentForm(request, initial={
                'invoice': 1,
                'amount': '12.50',
                'description': 'Золотое кольцо',
            })

            # можно сразу перенаправить
            return redirect(form.get_redirect_url())
            ...


            @receiver(gotobilling_success)
            def payment_success(sender, **kwargs):
                invoice = kwargs['invoice']
                request = kwargs['request']

            @receiver(gotobilling_error)
            def payment_error(sender, **kwargs):
                invoice = kwargs['invoice']
                request = kwargs['request']
                code = kwargs['code']
                reason = kwargs['reason']

        template.html:
            <form action="{{ form.target }}" method="post">
              {{ form.as_p }}
              <button type="submit">Pay</button>
            </form>

"""

default_app_config = 'gotobilling.apps.Config'
