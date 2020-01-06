from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'rating'
    verbose_name = _('Rating votes')

    def ready(self):
        from libs.js_storage import JS_STORAGE
        from django.core.urlresolvers import reverse

        JS_STORAGE.update({
            'ajax_vote': reverse('rating:vote'),
        })
