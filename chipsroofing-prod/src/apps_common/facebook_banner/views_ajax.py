from django.views.decorators.cache import cache_control
from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin


class BannerView(AjaxViewMixin, View):
    def get_handler(self, request):
        handler = super().get_handler(request)
        if handler:
            return cache_control(private=True, max_age=7*24*3600)(handler)
        else:
            return handler

    def get(self, request):
        return self.json_response({
            'html': self.render_to_string('facebook_banner/banner.html'),
        })
