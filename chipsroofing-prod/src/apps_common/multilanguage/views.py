from django.shortcuts import redirect
from libs.cookies import set_cookie
from .utils import noredirect_url, get_referer_url
from . import options


def redirect_to_language(request, code):
    """
        Переход на сайт с выбранным языком
    """
    referer_url = get_referer_url(request)

    # язык некорректен или отсутствует
    if not code or code not in options.MULTILANGUAGE_SITES:
        return redirect(referer_url)

    # запрещаем авторедирект на удаленном домене
    language = options.MULTILANGUAGE_SITES.get(code)
    redirect_url = noredirect_url(language['url'], forced_path=referer_url)

    # запрещаем авторедирект на текущем домене
    response = redirect(redirect_url)
    set_cookie(response, options.MULTILANGUAGE_COOKIE_KEY, '1', expires=365)
    return response
