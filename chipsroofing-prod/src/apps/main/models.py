from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from gallery.models import GalleryBase, GalleryImageItem
from apps.std_page.models import StdPage


class MainPageConfig(SingletonModel):
    """ Главная страница """
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('index')

    def __str__(self):
        return ugettext('Home page')
