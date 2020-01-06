import collections
from django.contrib import admin
from django.template import loader
from django.views.decorators.http import condition


class DecoratableViewMixin:
    """
        Представление, добавляющее метод get_handler,
        которое должно вернуть функцию(метод) обработки запроса.

        Этот метод может использоваться для декорирования методов CBV.
    """
    method = ''

    def get_handler(self, request):
        return getattr(self, self.method, None)

    def dispatch(self, request, *args, **kwargs):
        self.method = request.method.lower()
        if self.method not in self.http_method_names:
            return self.http_method_not_allowed(request, *args, **kwargs)

        handler = self.get_handler(request)
        if not callable(handler):
            return self.http_method_not_allowed(request, *args, **kwargs)

        return handler(request, *args, **kwargs)


class AdminViewMixin(DecoratableViewMixin):
    """
        Миксина для админской вьюхи
    """
    def get_handler(self, request):
        handler = super().get_handler(request)
        if handler:
            handler = admin.site.admin_view(handler)
        return handler


class CachedViewMixin(DecoratableViewMixin):
    """
        Миксина, добавляющая методы last_modified и etag,
        которые могут быть использованы для установки
        соответствующих заголовков в GET-запросах.

        Пример:
            class IndexView(CachedViewMixin, View):
                ...

                def last_modified(self, *args, **kwargs):
                    config =  ModuleConfig.get_solo()
                    return config.updated

    """
    def _last_modified(self, *args, **kwargs):
        """
            Обертка над реальным методом, обрабатывающая случаи,
            когда возвращается итератор
        """
        data = self.last_modified(*args, **kwargs)
        if isinstance(data, collections.Iterable):
            return max(filter(bool, data), default=None)
        else:
            return data

    def last_modified(self, *args, **kwargs):
        return None

    def etag(self, *args, **kwargs):
        return None

    def get_handler(self, request):
        handler = super().get_handler(request)
        if handler and self.method in ('get', 'head'):
            return condition(
                last_modified_func=self._last_modified,
                etag_func=self.etag,
            )(handler)
        else:
            return handler


class StringRenderMixin:
    """
        Представление, добавляющее метод render_to_string для
        рендеринга шаблона в строку.
    """
    def render_to_string(self, template, context=None, using=None):
        request = getattr(self, 'request', None)
        return loader.get_template(template, using=using).render(context, request)
