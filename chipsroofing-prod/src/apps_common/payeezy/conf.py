from django.conf import settings


# Обязательные параметры
LOGIN = settings.PAYEEZY_LOGIN
SEQUENCE = settings.PAYEEZY_SEQUENCE
TRANSACTION_KEY = settings.PAYEEZY_TRANSACTION_KEY
RESPONSE_KEY = settings.PAYEEZY_RESPONSE_KEY

# Encryption Type
ENCRYPTION_MD5 = 'md5'
ENCRYPTION_SHA1 = 'sha1'
ENCRYPTION_TYPE = getattr(settings, 'PAYEEZY_ENCRYPTION_TYPE', ENCRYPTION_MD5)

USE_POST = getattr(settings, 'PAYEEZY_USE_POST', True)
TEST_MODE = getattr(settings, 'PAYEEZY_TEST_MODE', False)

# Адрес, куда будет перенаправлен пользователь после успешной оплаты
SUCCESS_URL = getattr(
    settings,
    'PAYEEZY_SUCCESS_URL',
    settings.LOGIN_REDIRECT_URL
)

# Адрес, куда будет перенаправлен пользователь после неудачной оплаты
FAIL_URL = getattr(
    settings,
    'PAYEEZY_FAIL_URL',
    settings.LOGIN_REDIRECT_URL
)

# URL, по которому будет идти отправка форм
if TEST_MODE:
    FORM_TARGET = 'https://demo.globalgatewaye4.firstdata.com/payment'
else:
    FORM_TARGET = 'https://checkout.globalgatewaye4.firstdata.com/payment'
