from urllib.parse import urlencode
from django import forms
from django.shortcuts import resolve_url
from . import conf


FIELD_NAME_MAPPING = {
    'description': 'item_name',
    'address': 'address1',

    'recurring': 'src',
    'recurring_occurrences': 'srt',
    'recurring_trial_amount': 'a1',
    'recurring_trial_duration': 'p1',
    'recurring_trial_duration_unit': 't1',
    'recurring_amount': 'a3',
    'recurring_duration': 'p3',
    'recurring_duration_unit': 't3',

    'result_url': 'notify_url',
    'success_url': 'return',
    'cancel_url': 'cancel_return',
}


class BaseForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        kwargs.setdefault('auto_id', '')
        super().__init__(*args, **kwargs)

    def _get_value(self, fieldname):
        """ Получение значения поля формы """
        field = self.fields[fieldname]
        if self.is_bound:
            return self.cleaned_data.get(fieldname, field.initial)
        else:
            return self.initial.get(fieldname, field.initial)


class BasePayPalForm(BaseForm):
    target = conf.FORM_TARGET

    # аккаунт магазина
    business = forms.CharField(max_length=255, initial=conf.EMAIL)

    # кодировка
    charset = forms.CharField(max_length=32, required=False, initial='utf-8')

    # не требовать адрес доставки
    no_shipping = forms.CharField(max_length=1, required=False, initial='1')

    # не предлагать вводить примечание
    no_note = forms.CharField(max_length=1, required=False, initial='1')

    # адрес, обрабатывающий уведомления о платежах
    result_url = forms.URLField(max_length=255)

    # адреса для редиректа пользователей
    success_url = forms.URLField(max_length=1024)
    cancel_url = forms.URLField(max_length=1024)

    # Метод перехода на success_url (GET без параметров)
    rm = forms.CharField(max_length=1, initial='1')

    # Дополнительное поле для нужд разработчика
    custom = forms.CharField(max_length=256, required=False)

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        # Скрытие полей
        for name, field in self.fields.items():
            field.widget = field.hidden_widget()

        self.initial['result_url'] = request.build_absolute_uri(resolve_url(conf.RESULT_URL))
        self.initial['success_url'] = request.build_absolute_uri(resolve_url(conf.SUCCESS_URL))
        self.initial['cancel_url'] = request.build_absolute_uri(resolve_url(conf.CANCEL_URL))

    def add_prefix(self, field_name):
        """ Замена имен полей """
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super().add_prefix(field_name)

    def get_redirect_url(self):
        """
            Получить URL с GET-параметрами, соответствующими значениям полей в
            форме. Редирект на адрес, возвращаемый этим методом, эквивалентен
            ручной отправке формы методом GET.
        """
        params = {}
        for fieldname, field in self.fields.items():
            value = self._get_value(fieldname)
            if value:
                real_fieldname = FIELD_NAME_MAPPING.get(fieldname, fieldname)
                params[real_fieldname] = value

        return '{}?{}'.format(self.target, urlencode(params))


class PaymentForm(BasePayPalForm):
    """
        Форма для разового платежа
    """

    # Тип действия
    cmd = forms.CharField(max_length=32, initial='_xclick')

    # валюта оплаты
    currency_code = forms.CharField(max_length=3, initial=conf.CURRENCY)

    invoice = forms.CharField(max_length=127)
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
    description = forms.CharField(max_length=127)

    item_number = forms.CharField(max_length=127, required=False)
    quantity = forms.IntegerField(min_value=0, initial='1', required=False)

    # информация о плательщике
    first_name = forms.CharField(max_length=32, required=False)
    last_name = forms.CharField(max_length=32, required=False)
    address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=40, required=False)
    state = forms.CharField(max_length=2, required=False)
    zip = forms.CharField(max_length=32, required=False)
    country = forms.CharField(max_length=2, required=False)
    phone = forms.CharField(max_length=25, required=False)
    email = forms.CharField(max_length=127, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('recurring'):
            self.initial['cmd'] = '_xclick-subscriptions'


class SubscriptionForm(BasePayPalForm):
    """
        Форма для повторяющегося платежа
    """

    # Тип действия
    cmd = forms.CharField(max_length=32, initial='_xclick-subscriptions')

    # валюта оплаты
    currency_code = forms.CharField(max_length=3, initial=conf.CURRENCY)

    invoice = forms.CharField(max_length=127)
    description = forms.CharField(max_length=127)

    # Повторяющийся платеж
    recurring = forms.IntegerField(min_value=0, max_value=1, required=False, initial=1)
    recurring_amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2, initial=0)
    recurring_duration = forms.IntegerField(min_value=0, max_value=99, initial=1)
    recurring_duration_unit = forms.CharField(max_length=1, initial='M')

    recurring_occurrences = forms.IntegerField(min_value=2, max_value=52, required=False)

    recurring_trial_amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2, required=False)
    recurring_trial_duration = forms.IntegerField(min_value=0, max_value=99, required=False, initial=1)
    recurring_trial_duration_unit = forms.CharField(max_length=1, required=False, initial='M')

    # информация о плательщике
    first_name = forms.CharField(max_length=32, required=False)
    last_name = forms.CharField(max_length=32, required=False)
    address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=40, required=False)
    state = forms.CharField(max_length=2, required=False)
    zip = forms.CharField(max_length=32, required=False)
    country = forms.CharField(max_length=2, required=False)
    phone = forms.CharField(max_length=25, required=False)
    email = forms.CharField(max_length=127, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        trial_amount = self.initial.get('recurring_trial_amount')
        if trial_amount is None:
            del self.fields['recurring_trial_amount']
            del self.fields['recurring_trial_duration']
            del self.fields['recurring_trial_duration_unit']


class AddToCartForm(BasePayPalForm):
    """
        Форма для добавления товара в корзину PayPal
    """

    # Тип действия
    cmd = forms.CharField(max_length=32, initial='_cart')
    add = forms.CharField(max_length=1, initial='1')

    # валюта оплаты
    currency_code = forms.CharField(max_length=3, initial=conf.CURRENCY)

    invoice = forms.CharField(max_length=127)
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
    description = forms.CharField(max_length=127)

    item_number = forms.CharField(max_length=127, required=False)
    quantity = forms.IntegerField(min_value=0, initial='1', required=False)

    # Ссылка, куда переходит юзер, чтобы продолжить покупки
    shopping_url = forms.URLField(max_length=255, required=False)


class DisplayCartForm(BasePayPalForm):
    """
        Форма для просмотра корзины PayPal
    """

    # Тип действия
    cmd = forms.CharField(max_length=32, initial='_cart')
    display = forms.CharField(max_length=1, initial='1')

    # Ссылка, куда переходит юзер, чтобы продолжить покупки
    shopping_url = forms.URLField(max_length=255, required=False)


class DonationForm(BasePayPalForm):
    """
        Форма для пожертвований
    """

    # Тип действия
    cmd = forms.CharField(max_length=32, initial='_donations')

    # валюта оплаты
    currency_code = forms.CharField(max_length=3, initial=conf.CURRENCY)

    invoice = forms.CharField(max_length=127)
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
    description = forms.CharField(max_length=127)


class PayPalResultForm(forms.Form):
    """
        Форма для обработки результата оплаты
    """
    payment_status = forms.CharField(max_length=32)
    receiver_email = forms.EmailField()
    invoice = forms.CharField(max_length=127, required=False)
    mc_gross = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
    item_number = forms.CharField(max_length=127, required=False)
    quantity = forms.IntegerField(min_value=0, initial='1', required=False)
    custom = forms.CharField(max_length=256, required=False)
