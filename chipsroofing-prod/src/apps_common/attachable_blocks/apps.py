from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'attachable_blocks'
    verbose_name = _('Attachable blocks')

    def ready(self):
        from django.shortcuts import resolve_url
        from django.core.cache import cache
        from libs.js_storage import JS_STORAGE
        cache.delete('attachable_block_types')

        JS_STORAGE.update({
            'ajax_attached_block': resolve_url('blocks:ajax'),
        })
