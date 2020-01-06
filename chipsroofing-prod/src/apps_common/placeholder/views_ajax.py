import re
from collections import Iterable
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from libs.views_ajax import AjaxViewMixin
from .utils import PLACEHOLDERS

re_placeholder = re.compile(r'arr\[(\d+)\]\[([^\]]+)]')


class MiddlewareView(AjaxViewMixin, View):
    """
        Промежуточное представление, обрабатывающее все запросы на заглушки.
        Выделяет параметры частей заглушки и передает в представление заглушки.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, name=None, *args, **kwargs):
        if name is None:
            name = request.POST.get('name')

        if not name:
            return self.json_error({
                'error': _('empty placeholder name')
            })

        if name not in PLACEHOLDERS:
            return self.json_error({
                'error': _('unknown placeholder name')
            })

        # разбор частей заглушки из параметров запроса
        parts_dict = {}
        for key, value in request.POST.items():
            match = re_placeholder.fullmatch(key)
            if match is None:
                continue

            index = match.group(1)
            param_name = match.group(2)

            part = parts_dict.setdefault(index, {})
            if param_name != '_':
                part[param_name] = value

        # сортировка частей по индексам
        sorted_parts = sorted(parts_dict.items(), key=lambda kv: int(kv[0]))
        parts = tuple(params for index, params in sorted_parts)

        output = PLACEHOLDERS[name](request, name, parts)
        if isinstance(output, Iterable):
            output = tuple(output)
        else:
            output = (output, )

        return self.json_response({
            'parts': output,
        })
