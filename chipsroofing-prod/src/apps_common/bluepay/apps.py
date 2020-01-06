from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'bluepay'
    verbose_name = _('BluePay')
