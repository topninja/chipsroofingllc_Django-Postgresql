from django.conf import settings


# Обязательные параметры
MERCHANT_NAME = settings.BLUEPAY_MERCHANT_NAME
ACCOUNT_ID = settings.BLUEPAY_ACCOUNT_ID
USER_ID = settings.BLUEPAY_USER_ID
SECRET_KEY = settings.BLUEPAY_SECRET_KEY

# Тестовый режим
TEST_MODE = getattr(settings, 'BLUEPAY_TEST_MODE', False)

# URL, по которому будет идти отправка форм
FORM_TARGET = 'https://secure.bluepay.com/interfaces/shpf'


# Адрес страницы обработки результата
RESULT_URL = getattr(
    settings,
    'BLUEPAY_RESULT_URL',
    'bluepay:result'
)

# Адрес, куда будет перенаправлен пользователь после успешной оплаты
SUCCESS_URL = getattr(
    settings,
    'BLUEPAY_SUCCESS_URL',
    settings.LOGIN_REDIRECT_URL
)

# Адрес, куда будет перенаправлен пользователь после неудачной оплаты
FAIL_URL = getattr(
    settings,
    'BLUEPAY_FAIL_URL',
    settings.LOGIN_REDIRECT_URL
)
