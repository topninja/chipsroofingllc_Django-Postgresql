from django.views.generic import TemplateView
from libs.views import CachedViewMixin
from seo.seo import Seo
from .models import TestimonialsPageConfig, Testimonials
from django.template import Library, loader

register = Library()


class TestimonialsView(CachedViewMixin, TemplateView):
    template_name = 'testimonials/index.html'
    config = None

    def last_modified(self, *args, **kwargs):
        self.config = TestimonialsPageConfig.get_solo()
        return self.config.updated

    def get(self, request, *args, **kwargs):
        # SEO
        seo = Seo()
        seo.set_data(self.config)
        seo.save(request)

        request.breadcrumbs.add('TESTIMONIALS')

        return self.render_to_response({
            'testimonials': Testimonials.objects.filter(visible=True),
            'config': self.config,
            'page_data': self.config,
        })


def testimonials_block_render(context, block, **kwargs):
    return loader.render_to_string('testimonials/block.html', {
        'testimonials': Testimonials.objects.filter(visible=True)[:3],
        'block': block,
    }, request=context.get('request'))
