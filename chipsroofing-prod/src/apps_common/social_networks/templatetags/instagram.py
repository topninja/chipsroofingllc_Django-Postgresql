from django.template import loader, Library
from ..models import SocialConfig

register = Library()


@register.simple_tag(takes_context=True)
def instagram_widget(context, user_id=None, tag=None, limit=10):
    request = context.get('request')
    if not request:
        return ''

    config = SocialConfig.get_solo()
    return loader.render_to_string('social_networks/instagram.html', {
        'access_token': config.instagram_access_token,
        'user_id': user_id,
        'tag': tag,
        'limit': limit,
    }, request=request)
