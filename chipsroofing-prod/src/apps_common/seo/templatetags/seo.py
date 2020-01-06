from django.template import Library
from libs.cache.cached import cached
from ..models import Counter

register = Library()


@cached()
def get_counters(position):
    counters = Counter.objects.filter(position=position)
    if not counters:
        return ''

    content = '\n'.join(c.content for c in counters)
    return content


@register.simple_tag
def seo_counters(position):
    return get_counters(position)
