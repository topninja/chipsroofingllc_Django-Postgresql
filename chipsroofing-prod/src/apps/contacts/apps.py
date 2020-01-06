from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'contacts'
    verbose_name = _('Contacts')

    def ready(self):
        from django.shortcuts import resolve_url
        from libs.js_storage import JS_STORAGE

        JS_STORAGE.update({
            'ajax_contact': resolve_url('contacts:ajax_contact'),
            'ajax_free_estimate': resolve_url('contacts:ajax_free_estimate'),
        })
