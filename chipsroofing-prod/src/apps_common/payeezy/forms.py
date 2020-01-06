import hmac
import time
import hashlib
from urllib.parse import urlencode
from django import forms
from django.utils.translation import ugettext_lazy as _
from . import conf


FIELD_NAME_MAPPING = {
    'amount': 'x_amount',
    'first_name': 'x_first_name',
    'last_name': 'x_last_name',
    'company': 'x_company',
    'address': 'x_address',
    'city': 'x_city',
    'state': 'x_state',
    'zip': 'x_zip',
    'country': 'x_country',
    'phone': 'x_phone',
    'email': 'x_email',
    'invoice': 'x_invoice_num',
    'description': 'x_description',
}


class BasePayeezyForm(forms.Form):
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


class PaymentForm(BasePayeezyForm):
    """ Форма для совершения платежа """

    # Параметр с URL'ом, на который будет отправлена форма.
    # Может пригодиться для использования в шаблоне.
    target = conf.FORM_TARGET

    # Обязательные поля. Не имеет отношения к валидации формы.
    # Перечисляются поля, в которых должно быть заполнено
    # начальное значение при создании формы
    REQUIRE_INITIAL = ('invoice', 'amount', 'description')

    x_login = forms.CharField(max_length=20, initial=conf.LOGIN)
    x_fp_sequence = forms.CharField(max_length=128, initial=conf.SEQUENCE)
    x_show_form = forms.CharField(max_length=32, initial='PAYMENT_FORM')

    x_fp_timestamp = forms.IntegerField()
    x_fp_hash = forms.CharField(max_length=64)

    # имя плательщика
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    # название компании плательщика
    company = forms.CharField(max_length=50, required=False)

    # адрес плательщика
    address = forms.CharField(max_length=60, required=False)
    city = forms.CharField(max_length=40, required=False)
    state = forms.CharField(max_length=40, required=False)
    zip = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=60, required=False)

    # контакты плательщика
    phone = forms.CharField(max_length=25, required=False)
    email = forms.CharField(max_length=255, required=False)

    invoice = forms.CharField(max_length=20)
    description = forms.CharField(max_length=100, required=False)

    # сумма к оплате
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        if conf.TEST_MODE:
            self.fields['x_test_request'] = forms.CharField(
                required=False,
                initial='TRUE',
                widget=forms.HiddenInput,
            )

        for fieldname in self.REQUIRE_INITIAL:
            value = self.initial.get(fieldname)
            if not value:
                raise ValueError('"%s" field requires initial value' % fieldname)

        self.initial['x_fp_timestamp'] = int(time.time())
        self.initial['x_fp_hash'] = self.calc_signature()

    def add_prefix(self, field_name):
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super().add_prefix(field_name)

    def calc_signature(self):
        hash_str = '^'.join(map(str, (
            self._get_value('x_login'),
            self._get_value('x_fp_sequence'),
            self._get_value('x_fp_timestamp'),
            self._get_value('amount'),
            '',
        )))
        digestmod = hashlib.sha1 if conf.ENCRYPTION_TYPE == conf.ENCRYPTION_SHA1 else hashlib.md5
        hasher = hmac.new(conf.TRANSACTION_KEY.encode(), hash_str.encode(), digestmod=digestmod)
        return hasher.hexdigest()

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


class PayeezyResultForm(BasePayeezyForm):
    """
        Форма для обработки результата оплаты
    """
    SIGNATURE_FIELDS = ('x_trans_id', 'x_amount')

    RESPONSE_CODE_APPROVED = '1'
    RESPONSE_CODE_DECLINED = '2'
    RESPONSE_CODE_ERROR = '3'
    RESPONSE_CODES = (
        (RESPONSE_CODE_APPROVED, _('Approved')),
        (RESPONSE_CODE_DECLINED, _('Declined')),
        (RESPONSE_CODE_ERROR, _('Error')),
    )

    x_response_code = forms.ChoiceField(choices=RESPONSE_CODES)
    x_response_reason_text = forms.CharField(max_length=255)
    x_trans_id = forms.CharField(max_length=10, required=False)
    x_invoice_num = forms.CharField(max_length=20, required=False)
    x_amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)
    x_MD5_Hash = forms.CharField(max_length=64, required=False)
    x_SHA1_Hash = forms.CharField(max_length=64, required=False)

    def calc_signature(self):
        hash_params = [conf.RESPONSE_KEY, conf.LOGIN]
        for fieldname in self.SIGNATURE_FIELDS:
            value = self._get_value(fieldname)
            if value is None:
                hash_params.append('')
            elif fieldname == 'x_amount':
                # Force decimal places
                hash_params.append('%.2f' % value)
            else:
                hash_params.append(str(value))

        hash_data = ''.join(map(str, hash_params))

        digestmod = hashlib.sha1 if conf.ENCRYPTION_TYPE == conf.ENCRYPTION_SHA1 else hashlib.md5
        hash_value = digestmod(hash_data.encode()).hexdigest().upper()
        return hash_value

    def clean(self):
        hash_name = 'x_SHA1_Hash' if conf.ENCRYPTION_TYPE == conf.ENCRYPTION_SHA1 else 'x_MD5_Hash'

        try:
            signature = self.cleaned_data[hash_name].upper()
        except KeyError:
            raise forms.ValidationError(_('Undefined signature'))

        if signature != self.calc_signature():
            raise forms.ValidationError(_('Invalid signature'))

        return self.cleaned_data

