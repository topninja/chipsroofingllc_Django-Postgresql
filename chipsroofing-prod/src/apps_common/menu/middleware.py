from .utils import get_menus, activate_by_url


class MenuMiddleware:
    @staticmethod
    def process_request(request):
        """ Создание экземпляров меню """
        if not request.is_ajax():
            request._menus = get_menus(request)

    @staticmethod
    def process_template_response(request, response):
        """
            Если в меню нет активного пункта, пытаемся его определить по URL.
        """
        if request.is_ajax():
            return response

        menus = getattr(request, '_menus', None)
        if not menus:
            return response

        if request.path_info == '/':
            return response

        for menu in menus.values():
            activate_by_url(menu, request.path_info)

        return response
