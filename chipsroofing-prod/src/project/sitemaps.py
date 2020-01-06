from django.contrib.sitemaps import GenericSitemap
from main.models import MainPageConfig
from about.models import AboutPageConfig
from blog.models import BlogConfig, BlogPost
from contacts.models import ContactsConfig
from examples.models import ExamplesPageConfig
from faq.models import FaqConfig, Faq
from services.models import ServicesConfig, Service
from testimonials.models import TestimonialsPageConfig

mainpage = {
    'queryset': MainPageConfig.objects.all(),
    'date_field': 'updated',
}

about = {
    'queryset': AboutPageConfig.objects.all(),
    'date_field': 'updated',
}

blog = {
    'queryset': BlogConfig.objects.all(),
    'date_field': 'updated',
}

blog_post = {
    'queryset': BlogPost.objects.filter(visible=True),
    'date_field': 'updated',
}

contacts = {
    'queryset': ContactsConfig.objects.all(),
    'date_field': 'updated',
}

examples = {
    'queryset': ExamplesPageConfig.objects.all(),
    'date_field': 'updated',
}

faq = {
    'queryset': FaqConfig.objects.all(),
    'date_field': 'updated',
}

faq_questions = {
    'queryset': Faq.objects.filter(visible=True),
    'date_field': 'updated',
}

services = {
    'queryset': ServicesConfig.objects.all(),
    'date_field': 'updated',
}

services_page = {
    'queryset': Service.objects.filter(visible=True),
    'date_field': 'updated',
}

testimonials = {
    'queryset': TestimonialsPageConfig.objects.all(),
    'date_field': 'updated',
}

site_sitemaps = {
    'main': GenericSitemap(mainpage, changefreq='daily', priority=1),
    'blog': GenericSitemap(blog, changefreq='daily', priority=0.5),
    'blog_post': GenericSitemap(blog_post, changefreq='daily', priority=0.5),
    'services': GenericSitemap(services, changefreq='daily', priority=1),
    'services_page': GenericSitemap(services_page, changefreq='daily', priority=1),
    'faq': GenericSitemap(faq, changefreq='weekly', priority=0.5),
    'faq_questions': GenericSitemap(faq_questions, changefreq='weekly', priority=0.5),
    'examples': GenericSitemap(examples, changefreq='weekly', priority=0.5),
    'about': GenericSitemap(about, changefreq='weekly', priority=0.5),
    'contacts': GenericSitemap(contacts, changefreq='weekly', priority=0.5),
    'testimonials': GenericSitemap(testimonials, changefreq='weekly', priority=0.5),
}
