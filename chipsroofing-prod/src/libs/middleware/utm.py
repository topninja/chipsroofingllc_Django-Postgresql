from urllib.parse import urlencode
from libs.cookies import set_cookie


class UTMMiddleware:
    @staticmethod
    def process_response(request, response):
        if request.is_ajax():
            return response

        utm_labels = {
            key: value
            for key, value in request.GET.items()
            if key.lower().startswith('utm_')
        }

        if utm_labels:
            set_cookie(response, 'utm', urlencode(utm_labels))
        return response

