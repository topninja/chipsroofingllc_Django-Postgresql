from django import forms
from django.utils.timezone import now
from django.shortcuts import resolve_url
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from . import api
from . import conf


class BaseForm(forms.Form):
    def _get_value(self, fieldname):
        """ Получение значения поля формы """
        field = self.fields[fieldname]
        if self.is_bound:
            return self.cleaned_data.get(fieldname, field.initial)
        else:
            return self.initial.get(fieldname, field.initial)


class PaymentForm(BaseForm):
    """
        Форма, ведущая на hosted form.
    """
    target = conf.FORM_TARGET

    # Токен формы (получаем по API)
    token = forms.CharField(
        widget=forms.HiddenInput,
    )

    amount = forms.DecimalField(min_value=0, max_digits=18, decimal_places=2)
    invoice = forms.CharField(max_length=20)
    description = forms.CharField(max_length=255, required=False)

    email = forms.CharField(max_length=255, required=False)

    # информация о плательщике
    billing_first_name = forms.CharField(max_length=50, required=False)
    billing_last_name = forms.CharField(max_length=50, required=False)
    billing_company = forms.CharField(max_length=50, required=False)
    billing_address = forms.CharField(max_length=60, required=False)
    billing_city = forms.CharField(max_length=40, required=False)
    billing_state = forms.CharField(max_length=40, required=False)
    billing_zip = forms.CharField(max_length=20, required=False)
    billing_country = forms.CharField(max_length=60, required=False)
    billing_phone = forms.CharField(max_length=25, required=False)

    # доставка
    shipping_first_name = forms.CharField(max_length=50, required=False)
    shipping_last_name = forms.CharField(max_length=50, required=False)
    shipping_company = forms.CharField(max_length=50, required=False)
    shipping_address = forms.CharField(max_length=60, required=False)
    shipping_city = forms.CharField(max_length=40, required=False)
    shipping_state = forms.CharField(max_length=40, required=False)
    shipping_zip = forms.CharField(max_length=20, required=False)
    shipping_country = forms.CharField(max_length=60, required=False)

    def __init__(self, request, *args, **kwargs):
        kwargs.setdefault('auto_id', '')
        super().__init__(*args, **kwargs)

        # Скрытие полей
        for name, field in self.fields.items():
            field.widget = field.hidden_widget()

        self.initial['token'] = api.get_form_token(
            amount=self._get_value('amount'),
            invoice=self._get_value('invoice'),
            description=self._get_value('description'),
            email=self._get_value('email'),

            billing_firstname=self._get_value('billing_first_name'),
            billing_lastname=self._get_value('billing_last_name'),
            billing_company=self._get_value('billing_company'),
            billing_address=self._get_value('billing_address'),
            billing_city=self._get_value('billing_city'),
            billing_state=self._get_value('billing_state'),
            billing_zipcode=self._get_value('billing_zip'),
            billing_country=self._get_value('billing_country'),
            billing_phone=self._get_value('billing_phone'),

            shipping_firstname=self._get_value('shipping_first_name'),
            shipping_lastname=self._get_value('shipping_last_name'),
            shipping_company=self._get_value('shipping_company'),
            shipping_address=self._get_value('shipping_address'),
            shipping_city=self._get_value('shipping_city'),
            shipping_state=self._get_value('shipping_state'),
            shipping_zipcode=self._get_value('shipping_zip'),
            shipping_country=self._get_value('shipping_country'),

            merchantName=conf.MERCHANT_NAME,
            return_text=conf.RETURN_TEXT,
            return_url=request.build_absolute_uri(resolve_url(conf.RETURN_URL)),
            cancel_text=conf.CANCEL_TEXT,
            cancel_url=request.build_absolute_uri(resolve_url(conf.CANCEL_URL)),
            color=conf.COLOR,
            captcha=conf.CAPTCHA,
            shippingForm=conf.SHIPPING_FORM,
            shippingRequired=conf.SHIPPING_REQUIRED,
            billingForm=conf.BILLING_FORM,
            billingRequired=conf.BILLING_REQUIRED,
            emailField=conf.EMAIL_FIELD,
            emailRequired=conf.EMAIL_REQUIRED,
        )


class CCForm(BaseForm):
    """ Форма ввода данных кредитной карточки """
    number = forms.CharField(
        label=_('Card Number'),
        min_length=13,
        max_length=16
    )

    expiry_month = forms.IntegerField(
        label=_('MM'),
        min_value=1,
        max_value=12
    )

    expiry_year = forms.IntegerField(
        label=_('YYYY'),
    )

    cvv = forms.CharField(
        label=_('CVV'),
        min_length=3,
        max_length=4,
        validators=[RegexValidator(r'^[0-9]+$')]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = now().year
        self.fields['expiry_year'].min_value = current_year
        self.fields['expiry_year'].max_value = current_year + 20

    @property
    def expiry_date(self):
        if not self.is_bound:
            return

        return '{}-{:02}'.format(
            self.cleaned_data['expiry_year'],
            self.cleaned_data['expiry_month'],
        )


class EcheckForm(BaseForm):
    """ Форма ввода данных eCheck """
    routing_number = forms.CharField(
        label=_('Routing Number'),
        min_length=9,
        max_length=9,
        validators=[RegexValidator(r'^[0-9]+$')]
    )
    account_number = forms.CharField(
        label=_('Account Number'),
        min_length=8,
        max_length=17,
        validators=[RegexValidator(r'^[0-9]+$')]
    )
    name_on_account = forms.CharField(
        label=_('Name On Account'),
        max_length=22
    )
    bank_name = forms.CharField(
        label=_('Bank Name'),
        max_length=50
    )
    account_type = forms.ChoiceField(
        label=_('Account Type'),
        choices=conf.ECHECK_ACCOUNT_CHOICES,
        initial=conf.ECHECK_ACCOUNT_CHECKING
    )
