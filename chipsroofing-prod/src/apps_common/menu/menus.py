from django.utils.translation import ugettext_lazy as _
from .base import Menu, MenuItem


def main(request):
    menu = Menu()
    menu.append(
        MenuItem(
            title=_('About us'),
            url='about:index',
        ),
        MenuItem(
            title=_('Services'),
            url='services:index',
        ),
        MenuItem(
            title=_('FAQ'),
            url='faq:index',
        ),
        MenuItem(
            title=_('Work Examples'),
            url='examples:index',
        ),
        MenuItem(
            title=_('Blog'),
            url='blog:index',
        ),
        MenuItem(
            title=_('Contact us'),
            url='contacts:index',
        ),
    )
    return menu

def footer(request):
    menu = Menu()
    menu.append(
        MenuItem(
            title=_('About us'),
            url='about:index',
        ),
        MenuItem(
            title=_('Services'),
            url='services:index',
        ),
        MenuItem(
            title=_('FAQ'),
            url='faq:index',
        ),
        MenuItem(
            title=_('Work Examples'),
            url='examples:index',
        ),
        MenuItem(
            title=_('Blog'),
            url='blog:index',
        ),
        MenuItem(
            title=_('Contact'),
            url='contacts:index',
        ),
    )

    return menu


