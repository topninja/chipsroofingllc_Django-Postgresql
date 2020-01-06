from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'boxberry'
    verbose_name = _('Boxberry')

    def ready(self):
        from libs.js_storage import JS_STORAGE
        from .conf import KEY

        JS_STORAGE.update({
            'boxberry_key': KEY,
        })
