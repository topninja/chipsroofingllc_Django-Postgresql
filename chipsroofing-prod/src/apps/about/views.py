from django.views.generic import TemplateView
from libs.views import CachedViewMixin
from seo.seo import Seo
from .models import AboutPageConfig


class AboutView(CachedViewMixin, TemplateView):
    template_name = 'about/index.html'
    config = None

    def last_modified(self, *args, **kwargs):
        self.config = AboutPageConfig.get_solo()
        return self.config.updated

    def get(self, request, *args, **kwargs):
        # SEO
        seo = Seo()
        seo.set_data(self.config)
        seo.save(request)

        request.breadcrumbs.add('ABOUT US')

        return self.render_to_response({
            'config': self.config,
            'page_data': self.config,
        })
