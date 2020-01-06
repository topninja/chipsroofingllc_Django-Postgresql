from django.conf import settings
from . import JS_STORAGE


class JSStorageMiddleware:
    @staticmethod
    def process_request(request):
        request.js_storage = JS_STORAGE.copy()
        request.js_storage.update(
            cookie_domain=settings.SESSION_COOKIE_DOMAIN,
        )
