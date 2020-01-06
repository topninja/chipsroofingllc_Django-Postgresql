from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin
from .forms import SubscribeForm
from .utils import make_subscriber


class SubscribeView(AjaxViewMixin, View):
    def get(self, request):
        form = SubscribeForm()
        return self.json_response({
            'form': self.render_to_string('mailerlite/ajax_subscribe.html', {
                'form': form,
            }),
        })

    def post(self, request):
        form = SubscribeForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            subscriber = make_subscriber(email)

            groups = form.cleaned_data.get('groups')
            subscriber.groups.clear()
            subscriber.groups.add(*groups)

            return self.json_response({
                'success_message': self.render_to_string('mailerlite/ajax_subscribe_success.html')
            })
        else:
            return self.json_error({
                'errors': form.error_dict_full,
            }, status=400)
