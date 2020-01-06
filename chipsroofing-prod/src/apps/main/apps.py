from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'main'
    verbose_name = _('Home page')

    def ready(self):
        from django.shortcuts import resolve_url
        from libs.js_storage import JS_STORAGE

        JS_STORAGE.update({
            'ajax_main': resolve_url('ajax_main'),
        })