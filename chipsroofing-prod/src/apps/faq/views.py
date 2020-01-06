from django.db import models
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from libs.views import CachedViewMixin
from seo.seo import Seo
from .models import FaqConfig, Faq
from django.template import Library, loader

register = Library()


class IndexView(CachedViewMixin, TemplateView):
    template_name = 'faq/index.html'
    config = None

    def last_modified(self, *args, **kwargs):
        self.config = FaqConfig.get_solo()
        return self.config.updated

    def get(self, request, *args, **kwargs):
        # SEO
        seo = Seo()
        seo.set_data(self.config)
        seo.save(request)

        request.breadcrumbs.add("FAQ's")

        return self.render_to_response({
            'config': self.config,
            'page_data': self.config,
            'is_faq_page': True
        })


class DetailView(CachedViewMixin, TemplateView):
    template_name = 'faq/detail.html'
    config = None
    question = None

    def last_modified(self, *args, slug=None, **kwargs):
        self.config = FaqConfig.get_solo()
        self.question = get_object_or_404(Faq, slug=slug)
        return self.config.updated, self.question.updated

    def get(self, request, *args, slug=None, **kwargs):
        # SEO
        seo = Seo()
        seo.set_data(self.question, defaults={
            'title': self.question.title,
        })
        seo.save(request)

        request.breadcrumbs.add(self.config)
        request.breadcrumbs.add(self.question)

        return self.render_to_response({
            'config': self.config,
            'page_data': self.question,
            'detail_page_blocks': self.question,
        })


def faq_block_render(context, block, **kwargs):
    faqs = Faq.objects.filter(visible=True)
    page_data = context.get('page_data')

    if page_data:
        if isinstance(page_data, Faq):
            faqs = faqs.exclude(pk=page_data.pk)

    return loader.render_to_string('faq/block.html', {
        'is_faq_page': context.get('is_faq_page'),
        'faqs': faqs,
        'block': block,
    }, request=context.get('request'))
