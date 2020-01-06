from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin
from services.models import Service


class PopupView(AjaxViewMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        config = Service.objects.all()
        param = request.POST.get('param')

        return self.json_response({
            'service_popup': self.render_to_string('main/popup.html', {
                'services': config,
                'param': param
            })
        })
