from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'files'
    verbose_name = _('Files on Page')

    def ready(self):
        from .signals import handlers
