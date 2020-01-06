from django.template import Library, loader

register = Library()


@register.simple_tag(takes_context=True)
def menu(context, name, template='menu/menu.html'):
    request = context.get('request')
    if not request:
        return ''

    menus = getattr(request, '_menus', None)
    if not menus:
        return ''

    return loader.render_to_string(template, {
        'level': 1,
        'items': menus.get(name, ()),
    }, request=context.get('request'))
