from django.db import models
from libs.stdimage.fields import StdImageField
from libs.storages.media_storage import MediaStorage
from ckeditor.fields import CKEditorUploadField
from django.utils.translation import ugettext_lazy as _, ugettext


class StdPage(models.Model):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    background = StdImageField(_('Header image'),
                               storage=MediaStorage('std_page/header'),
                               min_dimensions=(900, 0),
                               admin_variation='admin',
                               crop_area=True,
                               null=True,
                               blank=True,
                               variations=dict(
                                   normal=dict(
                                       size=(1090, 420),
                                       crop=True
                                   ),
                                   tablet=dict(
                                       size=(600, 0),
                                       crop=False
                                   ),
                                   mobile=dict(
                                       size=(290, 140),
                                       crop=False
                                   ),
                                   admin=dict(
                                       size=(300, 150),
                                       crop=True
                                   ),
                               ),
                               )
    background_alt = models.CharField(_('Header image alt'), max_length=255, blank=True, help_text=_('for SEO'))
    text = CKEditorUploadField(_('Content block'), blank=True)
    text_second = CKEditorUploadField(_('Content second block'), blank=True)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        abstract = True
        default_permissions = ('change',)
        verbose_name = _('settings')

    def __str__(self):
        return ugettext('Page content')
