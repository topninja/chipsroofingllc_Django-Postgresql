from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'payeezy'
    verbose_name = _('Payeezy')
