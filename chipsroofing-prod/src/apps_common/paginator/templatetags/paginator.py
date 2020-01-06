from django.template import Library, loader

register = Library()


@register.simple_tag(takes_context=True)
def paginator(context, paginator, template='paginator/paginator.html'):
    request = context.get('request')

    if not paginator.current_page.has_other_pages():
        return ''

    return loader.render_to_string(template, {
        'paginator': paginator,
        'current_page_number': paginator.current_page_number,
    }, request=request)


@register.simple_tag
def href(paginator, number):
    """ Генерация ссылки на страницу навигации """
    return paginator.link_to(number)
