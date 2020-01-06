from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'placeholder'
    verbose_name = _('Placeholders')

    def ready(self):
        from django.shortcuts import resolve_url
        from libs.js_storage import JS_STORAGE

        JS_STORAGE.update({
            'placeholder_url': resolve_url('placeholder:ajax'),
        })
