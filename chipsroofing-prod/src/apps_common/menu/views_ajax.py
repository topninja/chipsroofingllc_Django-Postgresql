from django.template import loader
from libs.cache.cached import cached
from .utils import get_menus, activate_by_url


@cached('params.menu_name', 'params.referer', 'params.template', time=10*60)
def build_menu_part(request, name, **params):
    menus = get_menus(request)

    menu_name = params.get('menu_name')
    if not menu_name:
        return ''

    menu = menus.get(menu_name, ())

    referer = params.get('referer')
    if referer:
        activate_by_url(menu, referer)

    template = params.get('template')
    if not template:
        template = 'menu/menu.html'

    return loader.render_to_string(template, {
        'level': 1,
        'items': menu,
    }, request=request)


def menu_placeholder(request, name, parts):
    return [build_menu_part(request, name, **part_params) for part_params in parts]
