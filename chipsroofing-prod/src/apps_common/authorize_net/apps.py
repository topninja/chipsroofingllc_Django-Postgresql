from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'authorize_net'
    verbose_name = _('Authorize.Net')
