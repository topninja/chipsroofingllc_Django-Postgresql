from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'menu'
    verbose_name = _('Menu')

    def ready(self):
        from placeholder.utils import register_placeholder
        from .views_ajax import menu_placeholder
        register_placeholder('menu', menu_placeholder)
