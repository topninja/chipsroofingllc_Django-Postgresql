from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'blog'
    verbose_name = _('Blog')

    def ready(self):
        from django.shortcuts import resolve_url
        from libs.js_storage import JS_STORAGE

        JS_STORAGE.update({
            'ajax_blog': resolve_url('blog:ajax_blog'),
        })
