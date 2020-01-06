from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    label = 'pipeline_plus'
    name = 'libs.pipeline'
    verbose_name = _('Pipeline')
