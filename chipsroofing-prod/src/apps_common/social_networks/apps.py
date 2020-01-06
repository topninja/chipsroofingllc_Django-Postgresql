from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'social_networks'
    verbose_name = _('Social Media')

    def ready(self):
        from placeholder.utils import register_placeholder
        from .views_ajax import social_links_placeholder
        register_placeholder('social_links', social_links_placeholder)
