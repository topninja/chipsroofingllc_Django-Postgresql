from ipware.ip import get_ip
from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import is_valid_path
from libs.geocity.api import info
from libs.cookies import set_cookie
from .utils import noredirect_url
from . import options


class LanguageRedirectMiddleware:
    """
        Осуществляет редирект на сайт определенного языка,
        если в сессии не указано, что редирект запрещен.
    """
    @staticmethod
    def process_request(request):
        # Проверяем запрет авторедиректа через GET-параметр
        if request.GET.get(options.MULTILANGUAGE_GET_PARAM):
            request.disable_autoredirect = True

            # Проверяем, что на текущем сайте есть такая страница,
            # иначе, редиректим на MULTILANGUAGE_FALLBACK_URL
            urlconf = getattr(request, 'urlconf', None)
            if not is_valid_path(request.path_info, urlconf):
                return redirect(options.MULTILANGUAGE_FALLBACK_URL)

            return

        # Проверяем запрет авторедиректа через куку
        if request.COOKIES.get(options.MULTILANGUAGE_COOKIE_KEY, None):
            return

        # Проверяем запрет авторедиректа для определенных User-Agent
        ua_string = request.META.get('HTTP_USER_AGENT', '').lower()
        for pattern in options.ROBOTS_UA:
            if pattern in ua_string:
                return

        # Получение информации о IP
        ip = get_ip(request)
        ip_info = info(ip, detailed=True)
        if not ip_info:
            request.disable_autoredirect = True
            return

        # Определение кода языка, на который нужно редиректить
        current_code = settings.LANGUAGE_CODE
        redirect_code = current_code
        try:
            ip_iso = ip_info.get('country').get('iso')
        except AttributeError:
            pass
        else:
            for code, opts in options.MULTILANGUAGE_SITES.items():
                iso = opts.get('iso')
                if iso and ip_iso in iso:
                    redirect_code = code
                    break

        if current_code != redirect_code:
            request.disable_autoredirect = True
            language = options.MULTILANGUAGE_SITES.get(redirect_code)
            if language:
                redirect_url = noredirect_url(language['url'], forced_path=request.path)
                return redirect(redirect_url)

    @staticmethod
    def process_response(request, response):
        if getattr(request, 'disable_autoredirect', None) is True:
            set_cookie(response, options.MULTILANGUAGE_COOKIE_KEY, '1', expires=365)

        return response
