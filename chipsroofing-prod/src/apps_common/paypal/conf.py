from django.conf import settings


# Обязательные параметры
EMAIL = settings.PAYPAL_EMAIL
CURRENCY = settings.PAYPAL_CURRENCY

# Включен ли тестовый режим
TEST_MODE = getattr(settings, 'PAYPAL_TEST_MODE', False)
if TEST_MODE:
    FORM_TARGET = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
else:
    FORM_TARGET = 'https://www.paypal.com/cgi-bin/webscr'

# Адрес страницы обработки результата
RESULT_URL = getattr(
    settings,
    'PAYPAL_RESULT_URL',
    'paypal:result'
)

# Адрес, куда будет перенаправлен пользователь после успешной оплаты
SUCCESS_URL = getattr(
    settings,
    'PAYPAL_SUCCESS_URL',
    '/'
)

# Адрес, куда будет перенаправлен пользователь после неудачной оплаты
CANCEL_URL = getattr(
    settings,
    'PAYPAL_CANCEL_URL',
    '/'
)
