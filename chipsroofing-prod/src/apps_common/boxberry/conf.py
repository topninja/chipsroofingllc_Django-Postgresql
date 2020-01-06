from django.conf import settings

# Ключ интеграции для виджета
KEY = getattr(settings, 'BOXBERRY_KEY')

# Ключ и URL для API
IS_TEST = getattr(settings, 'BOXBERRY_TEST', False)
if IS_TEST:
    API_TOKEN = getattr(settings, 'BOXBERRY_API_TEST_TOKEN', '')
    API_URL = 'http://test.api.boxberry.de/json.php'
else:
    API_TOKEN = getattr(settings, 'BOXBERRY_API_TOKEN', '')
    API_URL = 'http://api.boxberry.de/json.php'
