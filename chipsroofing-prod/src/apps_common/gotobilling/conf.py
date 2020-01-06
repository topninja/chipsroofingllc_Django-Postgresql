from django.conf import settings


# Обязательные параметры: Merchant ID и Gateway Hash
LOGIN = settings.GOTOBILLING_MID
HASH = settings.GOTOBILLING_HASH

# Адрес страницы обработки результата
RESULT_URL = getattr(
    settings,
    'GOTOBILLING_RESULT_URL',
    'gotobilling:result'
)

# Адрес, куда будет перенаправлен пользователь после успешной оплаты
SUCCESS_URL = getattr(
    settings,
    'GOTOBILLING_SUCCESS_URL',
    settings.LOGIN_REDIRECT_URL
)

# Адрес, куда будет перенаправлен пользователь после неудачной оплаты
FAIL_URL = getattr(
    settings,
    'GOTOBILLING_FAIL_URL',
    settings.LOGIN_REDIRECT_URL
)

# URL, по которому будет идти отправка форм
FORM_TARGET = 'https://secure.gotoBilling.com/gateway/transact.php'
