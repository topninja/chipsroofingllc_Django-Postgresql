from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'promocodes'
    verbose_name = _('Promo codes')
