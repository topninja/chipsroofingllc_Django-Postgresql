"""
    Модуль оплаты через FirstData Payeezy.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'payeezy',
                ...
            )

            PAYEEZY_LOGIN = 'HCO-TEST-632'
            PAYEEZY_SEQUENCE = 'somesequence'
            PAYEEZY_TRANSACTION_KEY = 'KRDlckOM~HRpb9hpLZj2'
            PAYEEZY_RESPONSE_KEY = 'glsqzYPTJXwTDek_iMXo'
            PAYEEZY_SUCCESS_URL = 'shop:index'
            PAYEEZY_FAIL_URL = 'shop:index'

            SUIT_CONFIG = {
                ...
                {
                    'app': 'payeezy',
                    'icon': 'icon-shopping-cart',
                    'models': (
                        'log',
                    )
                },
                ...
            }

        urls.py:
            ...
            url(r'^payeezy/', include('payeezy.urls', namespace='payeezy')),
            ...

    Настройки (settings.py):
        PAYEEZY_LOGIN = 'HCO-TEST-632'
        PAYEEZY_SEQUENCE = 'somesequence'
        PAYEEZY_TRANSACTION_KEY = 'KRDlckOM~HRpb9hpLZj2'
        PAYEEZY_RESPONSE_KEY = 'glsqzYPTJXwTDek_iMXo'

        # Используется ли метод POST для возврата на сайт
        PAYEEZY_USE_POST = True

        # Тестовый режим
        PAYEEZY_TEST_MODE = False

        # Метод хэширования (md5 / sha1)
        PAYEEZY_ENCRYPTION_TYPE = 'md5'

        # Адрес страницы, куда перенаправит пользователя
        # после успешной оплаты
        PAYEEZY_SUCCESS_URL = 'shop:index'

        # Адрес страницы, куда перенаправит пользователя
        # после неудачной оплаты
        PAYEEZY_FAIL_URL = 'shop:index'

    Пример:
        views.py:
            from payeezy.forms import PaymentForm
            from payeezy.signals import payeezy_success, payeezy_error

            ...
            form = PaymentForm(initial={
                'invoice': 1,
                'amount': '12.50',
                'description': 'Золотое кольцо',
            })

            # можно сразу перенаправить
            return redirect(form.get_redirect_url())
            ...

            @receiver(payeezy_success)
            def payment_success(sender, **kwargs):
                invoice = kwargs['invoice']
                request = kwargs['request']

        template.html:
            <form action="{{ form.target }}" method="post">
              {{ form.as_p }}
              <button type="submit">Pay</button>
            </form>

"""

default_app_config = 'payeezy.apps.Config'
