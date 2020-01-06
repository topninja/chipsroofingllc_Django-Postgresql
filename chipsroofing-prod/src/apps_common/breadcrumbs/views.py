from django.template import loader


def render_breadcrumbs(breadcrumbs, template=None):
    if not breadcrumbs:
        return ''
    template = template or 'breadcrumbs/block.html'
    return loader.render_to_string(template, {
        'breadcrumbs': breadcrumbs,
    })
