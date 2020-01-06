from django.template import Library, loader
from contacts.models import Address

register = Library()


@register.simple_tag(takes_context=True)
def header(context, template='header/header.html'):
    """ Шапка """
    return loader.render_to_string(template, {
        'is_main_page': context.get('is_main_page'),
        'address': Address.objects.get(),
    }, request=context.get('request'))
