from django.template import loader, Library
from ..models import SocialLinks

register = Library()


@register.simple_tag(takes_context=True)
def social_links(context, classes='', template='social_networks/social_links.html'):
    request = context.get('request')
    if not request:
        return ''

    return loader.render_to_string(template, {
        'links': SocialLinks.get_solo(),
        'classes': classes,
    }, request=request)
