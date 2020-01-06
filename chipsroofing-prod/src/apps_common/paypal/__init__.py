"""
    Модуль оплаты через PayPal.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'paypal',
                ...
            )

            PAYPAL_TEST_MODE = True
            PAYPAL_EMAIL = 'x896321475-facilitator@gmail.com'
            PAYPAL_CURRENCY = 'USD'
            PAYPAL_SUCCESS_URL = 'shop:index'
            PAYPAL_CANCEL_URL = 'shop:index'

            SUIT_CONFIG = {
                ...
                {
                    'app': 'paypal',
                    'icon': 'icon-shopping-cart',
                },
                ...
            }

        urls.py:
            ...
            url(r'^paypal/', include('paypal.urls', namespace='paypal')),
            ...

    Пример:
        views.py:
            from paypal.forms import PaymentForm, SubscriptionForm, AddToCartForm, DisplayCartForm, DonationForm
            from paypal.signals import paypal_success

            ...
            # форма мгновенной оплаты
            form = PaymentForm(request, initial={
                'invoice': 18,
                'amount': '12.50',
                'description': 'Золотое кольцо',
                'quantity': 2,      // 2 штуки
            })

            # форма подписки
            form = SubscriptionForm(request, initial={
                'invoice': 18,
                'recurring_amount': '1.50',
                'description': 'Золотое кольцо',
            })

            # форма добавления товара в корзину
            add_cart_form = AddToCartForm(request, initial={
                'invoice': 18,
                'amount': '12.50',
                'description': 'Золотое кольцо',
                'quantity': 2,      // 2 штуки
            })

            # форма для просмотра корзины
            display_cart_form = DisplayCartForm(request, initial={
                'invoice': 18,
            })

            # форма для пожертвований
            donate_form = DonationForm(request, initial={
                'amount': '10.00',
                'description': 'На еду',
            })


            # можно сразу перенаправить
            return redirect(form.get_redirect_url())
            ...


            @receiver(paypal_success)
            def payment_success(sender, **kwargs):
                invoice = kwargs['invoice']
                request = kwargs['request']
                items = kwargs['items']

        template.html:
            <form action="{{ form.target }}" method="post">
              {{ form.as_p }}
              <button type="submit">Pay</button>
            </form>

"""

default_app_config = 'paypal.apps.Config'
