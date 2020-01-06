from urllib.parse import urlencode
from collections import defaultdict
from django.template import loader, Library

register = Library()


def vk(social_data):
    return 'http://vk.com/share.php?%s' % urlencode({
        'url': social_data['url'],
        'title': social_data['title'],
        'image': social_data['image'],
        'description': social_data['description'],
    })


def fb(social_data):
    return 'http://www.facebook.com/sharer/sharer.php?%s' % urlencode({
        'u': social_data['url'],
    })


def tw(social_data):
    from ..api.twitter import format_message
    return 'http://twitter.com/share?%s' % urlencode({
        'url': social_data['url'],
        'text': format_message(social_data['description']),
    })


def gp(social_data):
    return 'https://plus.google.com/share?%s' % urlencode({
        'url': social_data['url'],
    })


def li(social_data):
    from ..api.linkedin import format_message
    return 'http://www.linkedin.com/shareArticle?%s' % urlencode({
        'mini': 'true',
        'url': social_data['url'],
        'title': social_data['title'],
        'image': social_data['image'],
        'summary': format_message(social_data['description']),
    })


def pn(social_data):
    return 'http://www.pinterest.com/pin/create/button/?%s' % urlencode({
        'url': social_data['url'],
        'media': social_data['image'],
        'description': social_data['description'],
    })


@register.simple_tag(takes_context=True)
def share_button(context, provider, text='', url='', title='', description='', image=''):
    request = context.get('request')
    if not request:
        return ''

    social_data = defaultdict(lambda: '')

    # Берем данные из Opengraph
    seo = getattr(request, 'seo', None)
    if seo is not None:
        opengraph = seo['opengraph']
        social_data.update(opengraph._dict)

    # Возможность переопределения
    if url:
        social_data['url'] = url
    if title:
        social_data['title'] = title
    if description:
        social_data['description'] = description
    if image:
        social_data['image'] = image

    # Построение URL для расшаривания
    provider = provider.lower()
    if provider == 'vk':
        share_url = vk(social_data)
    elif provider == 'fb':
        share_url = fb(social_data)
    elif provider == 'tw':
        share_url = tw(social_data)
    elif provider == 'gp':
        share_url = gp(social_data)
    elif provider == 'li':
        share_url = li(social_data)
    elif provider == 'pn':
        share_url = pn(social_data)
    else:
        return ''

    return loader.render_to_string('social_networks/share_button.html', {
        'share_url': share_url,
        'provider': provider,
        'text': text,
    }, request=request)
