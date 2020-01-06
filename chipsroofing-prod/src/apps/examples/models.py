from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from gallery.fields import GalleryField
from gallery.models import GalleryBase, GalleryImageItem
from apps.std_page.models import StdPage
from attachable_blocks.models import AttachableBlock


class ExamplesImageItem(GalleryImageItem):
    STORAGE_LOCATION = 'examples/img_items'
    MIN_DIMENSIONS = (160, 120)
    ADMIN_CLIENT_RESIZE = True

    ASPECTS = 'desktop'
    SHOW_VARIATION = None
    ADMIN_VARIATION = 'admin'
    VARIATIONS = dict(
        desktop=dict(
            size=(980, 540),
        ),
        preview=dict(
            size=(235, 170),
        ),
        admin=dict(
            size=(160, 120),
        ),
    )


class Examples(GalleryBase):
    IMAGE_MODEL = ExamplesImageItem


class ExamplesPageConfig(SingletonModel, StdPage):
    gallery = GalleryField(Examples, verbose_name=_('gallery'), null=True)

    class Meta:
        default_permissions = ('change',)
        verbose_name = _('Settings')

    def get_absolute_url(self):
        return resolve_url('examples:index')

    def __str__(self):
        return ugettext('Examples')


class ExamplesBlock(AttachableBlock):
    BLOCK_VIEW = 'examples.views.examples_block_render'
    header = models.CharField(_('header'), max_length=128, blank=True)

    class Meta:
        verbose_name = _('Examples block')
        verbose_name_plural = _('Examples block')
