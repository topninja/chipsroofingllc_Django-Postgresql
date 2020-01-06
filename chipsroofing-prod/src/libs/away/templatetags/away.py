from django import template
from ..away import away_links

register = template.Library()


@register.simple_tag(takes_context=True)
def away(context, html):
    request = context.get('request')
    if not request:
        return html

    return away_links(request, html)
