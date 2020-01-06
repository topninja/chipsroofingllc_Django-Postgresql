from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'facebook_banner'
    verbose_name = _('Facebook Banner')

    def ready(self):
        from libs.js_storage import JS_STORAGE
        from django.core.urlresolvers import reverse
        from . import conf

        JS_STORAGE.update({
            'fb_banner_timeout': conf.POPUP_TIMEOUT,
            'fb_banner_url': reverse('facebook_banner:ajax_facebook_banner'),
        })
