from django.template import loader
from libs.cache.cached import cached
from .models import SocialLinks


@cached('params.template', 'params.classes', time=10*60)
def social_links_part(request, **params):
    template = params.get('template')
    if not template:
        template = 'social_networks/social_links.html'

    return loader.render_to_string(template, {
        'links': SocialLinks.get_solo(),
        'classes': params.get('classes', ''),
    }, request=request)


def social_links_placeholder(request, name, parts):
    return [social_links_part(request, **part_params) for part_params in parts]
