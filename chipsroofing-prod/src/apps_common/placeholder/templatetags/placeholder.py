from django.template import Library, loader

register = Library()


@register.simple_tag
def placeholder(name, **kwargs):
    return loader.render_to_string('placeholder/placeholder.html', {
        'name': name,
        'params': kwargs,
    })


