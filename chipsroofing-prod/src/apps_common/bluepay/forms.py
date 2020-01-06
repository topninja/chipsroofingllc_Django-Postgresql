from hashlib import md5
from decimal import Decimal
from urllib.parse import urlencode
from django import forms
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from . import conf


FIELD_NAME_MAPPING = {
    'payment_template': 'SHPF_FORM_ID',
    'account': 'SHPF_ACCOUNT_ID',
    'mode': 'MODE',
    'transaction_type': 'TRANSACTION_TYPE',
    'merchant_name': 'DBA',

    'tps_fields': 'SHPF_TPS_DEF',
    'tps': 'SHPF_TPS',
    'secret_tps_fields': 'TPS_DEF',
    'secret_tps': 'TAMPER_PROOF_SEAL',

    'first_name': 'NAME1',
    'last_name': 'NAME2',
    'address': 'ADDR1',
    'city': 'CITY',
    'state': 'STATE',
    'zip': 'ZIPCODE',
    'country': 'COUNTRY',
    'phone': 'PHONE',
    'email': 'EMAIL',

    'amount': 'AMOUNT',
    'invoice': 'INVOICE_ID',
    'description': 'COMMENT',

    'redirect_url': 'REDIRECT_URL',
}


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_id', '')
        super().__init__(*args, **kwargs)

    def _get_value(self, fieldname):
        """ Получение значения поля формы """
        field = self.fields[fieldname]
        if self.is_bound:
            return self.cleaned_data.get(fieldname, field.initial)
        else:
            return self.initial.get(fieldname, field.initial)


class PaymentForm(BaseForm):
    """ Форма для совершения платежа """

    # Параметр с URL'ом, на который будет отправлена форма.
    # Может пригодиться для использования в шаблоне.
    target = conf.FORM_TARGET

    # Обязательные поля. Не имеет отношения к валидации формы.
    # Перечисляются поля, в которых должно быть заполнено
    # начальное значение при создании формы
    REQUIRE_INITIAL = ('invoice', 'amount')

    # Поля, по которым рассчитывается хэш
    SHPF_TPS_FIELDS = (
        'payment_template', 'account', 'tps_fields', 'transaction_type', 'merchant_name',
        'redirect_url', 'amount', 'invoice',
    )
    SECRET_TPS_FIELDS = (
        'account', 'transaction_type', 'mode', 'amount', 'invoice',
    )

    # шаблон платежной формы
    payment_template = forms.ChoiceField(choices=(
        ('mobileform01', _('Credit Card Only - White Vertical (mobile capable)')),
        ('default1v5', _('Credit Card Only - Gray Horizontal')),
        ('default7v5', _('Credit Card Only - Gray Horizontal Donation')),
        ('default7v5R', _('Credit Card Only - Gray Horizontal Donation with Recurring')),
        ('default3v4', _('Credit Card Only - Blue Vertical with card swipe')),
        ('mobileform02', _('Credit Card & ACH - White Vertical (mobile capable)')),
        ('default8v5', _('Credit Card & ACH - Gray Horizontal Donation')),
        ('default8v5R', _('Credit Card & ACH - Gray Horizontal Donation with Recurring')),
        ('mobileform03', _('ACH Only - White Vertical (mobile capable)')),
    ), initial='mobileform01')

    account = forms.CharField(max_length=32, initial=conf.ACCOUNT_ID)
    mode = forms.CharField(max_length=16, initial='TEST' if conf.TEST_MODE else 'LIVE')
    transaction_type = forms.CharField(max_length=16, initial='SALE')
    merchant_name = forms.CharField(max_length=64, initial=conf.MERCHANT_NAME)

    # Хэширование
    tps_fields = forms.CharField(max_length=255, initial=' '.join(
        FIELD_NAME_MAPPING.get(field, field)
        for field in SHPF_TPS_FIELDS
    ))
    tps = forms.CharField(max_length=32)
    secret_tps_fields = forms.CharField(max_length=255, initial=' '.join(
        FIELD_NAME_MAPPING.get(field, field)
        for field in SECRET_TPS_FIELDS
    ).replace('SHPF_ACCOUNT_ID', 'MERCHANT'))
    secret_tps = forms.CharField(max_length=32)

    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
    invoice = forms.CharField(max_length=64)
    description = forms.CharField(max_length=128, required=False)

    # имя плательщика
    first_name = forms.CharField(max_length=32, required=False)
    last_name = forms.CharField(max_length=32, required=False)
    address = forms.CharField(max_length=64, required=False)
    city = forms.CharField(max_length=32, required=False)
    state = forms.CharField(max_length=16, required=False)
    zip = forms.CharField(max_length=16, required=False)
    country = forms.CharField(max_length=64, required=False)
    phone = forms.CharField(max_length=16, required=False)
    email = forms.CharField(max_length=64, required=False)

    redirect_url = forms.URLField(max_length=1024)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_url(request, 'redirect_url', conf.RESULT_URL)

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        for fieldname in self.REQUIRE_INITIAL:
            value = self.initial.get(fieldname)
            if not value:
                raise ValueError('"%s" field requires initial value' % fieldname)

        self._fill_shpf_tps()

    def _fill_shpf_tps(self):
        """
            Рассчет хэша по полям.
        """
        hash_vars = [conf.SECRET_KEY]
        for field_name in self.SHPF_TPS_FIELDS:
            value = self._get_value(field_name)
            hash_vars.append(value)

        hash_data = ''.join(map(str, hash_vars))
        self.initial['tps'] = md5(hash_data.encode()).hexdigest()

        # secret_tps
        hash_vars = [conf.SECRET_KEY]
        for field_name in self.SECRET_TPS_FIELDS:
            value = self._get_value(field_name)
            hash_vars.append(value)

        hash_data = ''.join(map(str, hash_vars))
        self.initial['secret_tps'] = md5(hash_data.encode()).hexdigest()

    def add_prefix(self, field_name):
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super().add_prefix(field_name)

    def _initial_url(self, request, fieldname, default):
        """
            Добавление initial-значения в поле fieldname, которое является полной ссылкой
            на страницу
        """
        url = self.initial.get(fieldname, '')
        if url:
            if not url.startswith('http'):
                self.initial[fieldname] = request.build_absolute_uri(resolve_url(url))
            return

        self.initial[fieldname] = request.build_absolute_uri(resolve_url(default))

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


class ResultForm(BaseForm):
    """
        Форма для обработки результата оплаты
    """
    RESULT_APPROVED = 'APPROVED'
    RESULT_DECLINED = 'DECLINED'
    RESULT_ERROR = 'ERROR'
    RESULT_MISSING = 'MISSING'
    RESULTS = (
        (RESULT_APPROVED, _('Approved')),
        (RESULT_DECLINED, _('Declined')),
        (RESULT_ERROR, _('Error')),
        (RESULT_MISSING, _('Missing')),
    )

    Result = forms.ChoiceField(choices=RESULTS)
    MESSAGE = forms.CharField(max_length=255)
    INVOICE_ID = forms.CharField(max_length=64)
    AMOUNT = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
