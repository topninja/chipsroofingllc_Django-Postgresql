from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.http.response import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from libs.views import DecoratableViewMixin, AdminViewMixin, StringRenderMixin


class LazyJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super().default(obj)


class AjaxViewMixin(StringRenderMixin, DecoratableViewMixin):
    """
        Миксина для обработки AJAX-запросов.

        Добавляет проверку request.is_ajax и методы json_response и json_error.
        Метод json_error полностью аналогичен json_response, но по умолчанию
        имеет статут ответа 400 (Bad Request).
    """
    verify_ajax = True

    def get_handler(self, request):
        if self.verify_ajax and not request.is_ajax():
            return None
        else:
            return super().get_handler(request)

    @staticmethod
    def json_response(data=None, **kwargs):
        if data is None:
            data = {}

        defaults = {
            'encoder': LazyJSONEncoder
        }
        defaults.update(kwargs)
        return JsonResponse(data, **defaults)

    def json_error(self, data=None, **kwargs):
        kwargs.setdefault('status', 400)
        return self.json_response(data, **kwargs)


class AjaxAdminViewMixin(AdminViewMixin, AjaxViewMixin):
    """
        Миксина для обработки AJAX-запросов в админке.
    """
    pass
