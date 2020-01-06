from django.views.generic import TemplateView
from libs.views import CachedViewMixin
from seo.seo import Seo
from .models import ExamplesPageConfig
from django.template import Library, loader
from paginator.paginator import Paginator, EmptyPage
from django.http.response import Http404

register = Library()


class ExamplesView(CachedViewMixin, TemplateView):
    template_name = 'examples/index.html'
    config = None

    def last_modified(self, *args, **kwargs):
        self.config = ExamplesPageConfig.get_solo()
        return self.config.updated

    def get(self, request, *args, **kwargs):
        try:
            paginator = Paginator(
                request,
                object_list=self.config.gallery.image_items,
                per_page=20,
                page_neighbors=1,
                side_neighbors=1,
                allow_empty_first_page=False,
            )
        except EmptyPage:
            raise Http404
        # SEO
        seo = Seo()
        seo.set_data(self.config)
        seo.save(request)

        request.breadcrumbs.add('WORK EXAMPLES')

        return self.render_to_response({
            'config': self.config,
            'page_data': self.config,
            'paginator': paginator,

        })


def examples_block_render(context, block, **kwargs):
    return loader.render_to_string('examples/block.html', {
        'config': ExamplesPageConfig.objects.first(),
        'block': block,
    }, request=context.get('request'))
