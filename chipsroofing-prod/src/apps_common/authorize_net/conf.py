from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _


# Обязательные параметры
LOGIN_ID = getattr(settings, 'AUTHORIZENET_LOGIN_ID', None)
TRANSACTION_KEY = getattr(settings, 'AUTHORIZENET_TRANSACTION_KEY', None)
SIGNATURE_KEY = getattr(settings, 'AUTHORIZENET_SIGNATURE_KEY', None)

ECHECK_ACCOUNT_CHECKING = 'checking'
ECHECK_ACCOUNT_SAVINGS = 'savings'
ECHECK_ACCOUNT_CHOICES = (
    (ECHECK_ACCOUNT_CHECKING, _('Checking')),
    (ECHECK_ACCOUNT_SAVINGS, _('Savings')),
)

RECURRING_UNITS_DAYS = 'days'
RECURRING_UNITS_MONTHS = 'months'
RECURRING_UNITS_CHOICES = (
    (RECURRING_UNITS_DAYS, _('Days')),
    (RECURRING_UNITS_MONTHS, _('Months')),
)

# Включен ли тестовый режим
TEST_MODE = getattr(settings, 'AUTHORIZENET_TEST_MODE', False)
if TEST_MODE:
    FORM_TARGET = 'https://test.authorize.net/payment/payment'
else:
    FORM_TARGET = 'https://accept.authorize.net/payment/payment'

# Название магазина (не обязательно)
MERCHANT_NAME = getattr(settings, 'AUTHORIZENET_MERCHANT_NAME', '')

# Цвет кнопок и нижней границы полей формы
COLOR = getattr(settings, 'AUTHORIZENET_COLOR', '#008020')

# Добавлять на форму капчу
CAPTCHA = getattr(settings, 'AUTHORIZENET_CAPTCHA', False)

# Отображение формы счета
BILLING_FORM = getattr(settings, 'AUTHORIZENET_BILLING_FORM', True)
BILLING_REQUIRED = getattr(settings, 'AUTHORIZENET_BILLING_REQUIRED', False)

# Отображение поля Email
EMAIL_FIELD = getattr(settings, 'AUTHORIZENET_EMAIL_FIELD', True)
EMAIL_REQUIRED = getattr(settings, 'AUTHORIZENET_EMAIL_REQUIRED', False)

# Отображение формы адреса доставки
SHIPPING_FORM = getattr(settings, 'AUTHORIZENET_SHIPPING_FORM', False)
SHIPPING_REQUIRED = getattr(settings, 'AUTHORIZENET_SHIPPING_REQUIRED', False)

# Ссылка для возврата после оплаты
RETURN_TEXT = ugettext('Continue')
RETURN_URL = getattr(
    settings,
    'AUTHORIZENET_RETURN_URL',
    '/'
)

# Ссылка для отмены оплаты
CANCEL_TEXT = ugettext('Cancel')
CANCEL_URL = getattr(
    settings,
    'AUTHORIZENET_CANCEL_URL',
    '/'
)
