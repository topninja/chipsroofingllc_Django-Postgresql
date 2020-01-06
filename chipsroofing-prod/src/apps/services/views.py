from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from libs.views import CachedViewMixin
from seo.seo import Seo
from .models import ServicesConfig, Service
from django.template import Library, loader

register = Library()


class IndexView(CachedViewMixin, TemplateView):
    template_name = 'services/index.html'
    config = None

    def last_modified(self, *args, **kwargs):
        self.config = ServicesConfig.get_solo()
        return self.config.updated

    def get(self, request, *args, **kwargs):
        # SEO
        seo = Seo()
        seo.set_data(self.config)
        seo.save(request)

        request.breadcrumbs.add("SERVICES")

        return self.render_to_response({
            'config': self.config,
            'page_data': self.config,
            'is_service_page': True,
        })


class DetailView(CachedViewMixin, TemplateView):
    template_name = 'services/detail.html'
    config = None
    service = None

    def last_modified(self, *args, parent_slug=None, slug=None, **kwargs):
        self.config = ServicesConfig.get_solo()
        self.service = get_object_or_404(Service, slug=slug)
        self.other_services = Service.get_siblings(self.service, include_self=False).filter(visible=True)
        return self.config.updated, self.service.updated

    def get(self, request, *args, slug=None, **kwargs):
        # SEO
        seo = Seo()
        seo.set_data(self.service, defaults={
            'title': self.service.title,
        })
        seo.save(request)

        request.breadcrumbs.add(self.config)
        if self.service.parent:
            request.breadcrumbs.add(self.service.parent)
        request.breadcrumbs.add(self.service)

        return self.render_to_response({
            'config': self.service,
            'page_data': self.service,
            'detail_page_blocks': self.service,

            'services': Service.get_children(self.service).filter(visible=True),
            'sub_services': Service.get_siblings(self.service).filter(visible=True),
            'is_root_node': True if self.other_services.first() and self.other_services.first().is_root_node() else False,

            'is_service_blocks': True,
        })


def services_block_render(context, block, **kwargs):
    service = Service.objects.root_nodes().filter(visible=True)
    page_data = context.get('page_data')

    if page_data:
        if isinstance(page_data, Service):
            service = service.exclude(pk=page_data.pk)

    return loader.render_to_string('services/block.html', {
        'is_main_page': context.get('is_main_page'),
        'is_service_page': context.get('is_service_page'),
        'services': service,
        'block': block,
    }, request=context.get('request'))
