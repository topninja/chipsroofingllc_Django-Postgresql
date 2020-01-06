from django.conf import settings
from django.template import loader, Library
from django.utils.translation import get_language
from .. import options

register = Library()


@register.simple_tag(takes_context=True)
def select_language(context, current_code=None):
    request = context.get('request')
    if not request:
        return ''

    current_code = current_code or get_language()
    if not current_code or current_code not in options.MULTILANGUAGE_SITES:
        current_code = settings.LANGUAGE_CODE

    return loader.render_to_string('multilanguage/allowed_languages.html', {
        'current_code': current_code,
        'langs': options.MULTILANGUAGE_SITES,
    }, request=request)
