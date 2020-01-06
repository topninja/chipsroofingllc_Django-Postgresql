from django.template import Library, loader
from contacts.models import Address
from .. import conf

register = Library()


@register.simple_tag(takes_context=True)
def footer(context, template='footer/footer.html'):
    """ Футер """
    return loader.render_to_string(template, {
        'address': Address.objects.get(),

    }, request=context.get('request'))


@register.simple_tag(takes_context=True)
def dl_link(context, template='footer/dl_link.html'):
    request = context.get('request')
    if not request:
        return ''

    rule = conf.RULES.get(request.path_info)
    if rule:
        return loader.render_to_string(template, rule, request=request)

    return loader.render_to_string(template, {
        'url': 'https://directlinedev.com/',
        'title': 'Web Development',
        'fallback': True,
    }, request=request)
