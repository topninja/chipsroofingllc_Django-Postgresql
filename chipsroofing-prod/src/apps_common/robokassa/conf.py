from django.conf import settings


# Обязательные параметры - реквизиты магазина
LOGIN = settings.ROBOKASSA_LOGIN
PASSWORD1 = settings.ROBOKASSA_PASSWORD1
PASSWORD2 = settings.ROBOKASSA_PASSWORD2

# Используется ли метод POST при приеме результатов от ROBOKASSA
USE_POST = getattr(settings, 'ROBOKASSA_USE_POST', True)

# Включен ли тестовый режим
TEST_MODE = getattr(settings, 'ROBOKASSA_TEST_MODE', False)

# URL, по которому будет идти отправка форм
FORM_TARGET = 'https://auth.robokassa.ru/Merchant/Index.aspx'

# Список (list) названий дополнительных параметров, которые будут передаваться вместе с запросами.
# Имена параметров ДОЛЖНЫ начинаться с "shp_"
EXTRA_PARAMS = sorted(getattr(settings, 'ROBOKASSA_EXTRA_PARAMS', []))
