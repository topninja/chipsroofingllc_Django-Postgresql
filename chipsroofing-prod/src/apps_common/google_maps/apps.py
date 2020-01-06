from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'google_maps'
    verbose_name = _('Google Maps')
