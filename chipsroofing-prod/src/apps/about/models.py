from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from apps.std_page.models import StdPage


class AboutPageConfig(SingletonModel, StdPage):
    class Meta:
        default_permissions = ('change',)
        verbose_name = _('Settings')

    def get_absolute_url(self):
        return resolve_url('about:index')

    def __str__(self):
        return ugettext('About Us')
