from hashlib import md5
from urllib.parse import urlencode, quote_plus
from django import forms
from django.utils.translation import ugettext_lazy as _
from . import conf

FIELD_NAME_MAPPING = {
    'invoice': 'InvId',
    'amount': 'OutSum',
    'description': 'Desc',
    'email': 'Email',
}


class BaseRobokassaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_id', '')
        super().__init__(*args, **kwargs)

        # создаем дополнительные поля
        for key in conf.EXTRA_PARAMS:
            self.fields[key] = forms.CharField(required=False)
            if 'initial' in kwargs:
                self.fields[key].initial = kwargs['initial'].get(key, None)

    def _get_value(self, fieldname):
        """ Получение значения поля формы """
        field = self.fields[fieldname]
        if self.is_bound:
            return self.cleaned_data.get(fieldname, field.initial)
        else:
            return self.initial.get(fieldname, field.initial)

    def calc_signature(self):
        hash_params = []
        for fieldname in self.SIGNATURE_FIELDS:
            value = self._get_value(fieldname)
            if value is None:
                value = ''
            hash_params.append(str(value))

        hash_params.append(self.PASSWD)

        # extra
        for key in sorted(conf.EXTRA_PARAMS):
            value = self._get_value(key)
            if value is None:
                value = ''
            value = quote_plus(str(value))
            hash_params.append('%s=%s' % (key, value))

        hash_data = ':'.join(map(str, hash_params))
        hash_value = md5(hash_data.encode()).hexdigest().upper()
        return hash_value


class PaymentForm(BaseRobokassaForm):
    """
        Форма для совершения платежа
    """
    SIGNATURE_FIELDS = ('MrchLogin', 'amount', 'invoice')
    PASSWD = conf.PASSWORD1

    # Параметр с URL'ом, на который будет отправлена форма.
    target = conf.FORM_TARGET

    # Обязательные поля. Не имеет отношения к валидации формы.
    # Перечисляются поля, в которых должно быть заполнено
    # начальное значение при создании формы
    REQUIRE_INITIAL = ('invoice', 'amount', 'description')

    # login магазина в обменном пункте
    MrchLogin = forms.CharField(max_length=20, initial=conf.LOGIN)

    # Номер счета в магазине. Значение этого параметра должно быть уникальным для каждой оплаты
    invoice = forms.IntegerField(min_value=0)

    # сумма к оплате
    amount = forms.DecimalField(min_value=0, max_digits=20, decimal_places=2)

    # описание покупки. Эта информация отображается в интерфейсе ROBOKASSA и в Электронной квитанции
    description = forms.CharField(max_length=100)

    # e-mail пользователя
    email = forms.EmailField(required=False)

    # Кодировка, в которой отображается страница ROBOKASSA.
    Encoding = forms.CharField(max_length=16, initial='utf-8')

    # контрольная сумма MD5
    SignatureValue = forms.CharField(max_length=32)

    # Предлагаемый способ оплаты. Тот вариант оплаты, который Вы рекомендуете использовать своим покупателям.
    # https://merchant.roboxchange.com/WebService/Service.asmx/GetCurrencies?MerchantLogin=demo&language=ru
    IncCurrLabel = forms.CharField(max_length=32, required=False)

    # язык общения с клиентом (en или ru)
    Culture = forms.CharField(max_length=10, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['SignatureValue'].initial = self.calc_signature()

        # скрытый виджет по умолчанию
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

        if conf.TEST_MODE:
            self.fields['IsTest'] = forms.CharField(
                required=False,
                widget=forms.HiddenInput,
            )

        for fieldname in self.REQUIRE_INITIAL:
            value = self.initial.get(fieldname)
            if not value:
                raise ValueError('"%s" field requires initial value' % fieldname)

    def add_prefix(self, field_name):
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
            value = self.initial.get(fieldname, field.initial)
            if value:
                real_fieldname = FIELD_NAME_MAPPING.get(fieldname, fieldname)
                params[real_fieldname] = value

        if conf.TEST_MODE:
            params['IsTest'] = '1'

        return '{}?{}'.format(self.target, urlencode(params))


class ResultURLForm(BaseRobokassaForm):
    """
        Форма для обработки результата оплаты
    """
    SIGNATURE_FIELDS = ('OutSum', 'InvId')
    PASSWD = conf.PASSWORD2

    OutSum = forms.DecimalField(min_value=0, max_digits=20, decimal_places=6)
    InvId = forms.IntegerField(min_value=0, max_value=2147483647)
    SignatureValue = forms.CharField(max_length=32)

    def clean(self):
        try:
            signature = self.cleaned_data['SignatureValue'].upper()
        except KeyError:
            raise forms.ValidationError(_('Undefined signature'))

        if signature != self.calc_signature():
            raise forms.ValidationError(_('Invalid signature'))

        return self.cleaned_data
