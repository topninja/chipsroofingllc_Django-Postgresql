"""
    Модуль оплаты через Authorize.NET.

    Зависит от:
        ipware
        authorizenet

    Создание Sandbox:
        1) Регистрация:
            https://developer.authorize.net/hello_world/sandbox/
        2) Установить MD5 Hash:
            Account -> Settings -> MD5 Hash
        3) Получить Signature Key
            Account -> Settings -> API Credentials & Keys
        4) Установить Webhook на Payment Events
            Account -> Settings -> Webhook
        5) Разрешить Transaction Detail API
            Account -> Settings -> Transaction Details API

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'authorize_net',
                ...
            )

            AUTHORIZENET_LOGIN_ID = '6Kz7p89GX2'
            AUTHORIZENET_TRANSACTION_KEY = '86aLNBsv68w9924W'
            AUTHORIZENET_SIGNATURE_KEY = '31E165E98F7DAB6C5D26CE33C8E8FD46D3B7117B033221DEE0B4E54B4FA9EF3C21435F2CDF6626ABA1F4A040654080F9B856797D1337FC92A4B65730CB168B99'
            AUTHORIZENET_TEST_MODE = False
            AUTHORIZENET_RETURN_URL = 'shop:index'
            AUTHORIZENET_CANCEL_URL = 'shop:index'

            SUIT_CONFIG = {
                ...
                {
                    'app': 'authorize_net',
                    'icon': 'icon-shopping-cart',
                },
                ...
            }

        urls.py:
            ...
            url(r'^authorize_net/', include('authorize_net.urls', namespace='authorize_net')),
            ...

    Пример:
        views.py:
            from authorize_net.forms import PaymentForm
            from authorize_net.signals import authorizenet_success

            ...
            form = PaymentForm(request, initial={
                'invoice': 1,
                'amount': '12.50',
                'description': 'Golden Ring',
            })

            @receiver(authorizenet_success)
            def payment_success(sender, request, amount, invoice, **kwargs):
                pass

        template.html:
            <form action="{{ form.target }}" method="post">
              {{ form }}
              <button type="submit">Pay</button>
            </form>

"""

default_app_config = 'authorize_net.apps.Config'
