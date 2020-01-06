from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from ckeditor.fields import CKEditorUploadField
from libs.autoslug import AutoSlugField
from attachable_blocks.models import AttachableBlock
from apps.std_page.models import StdPage
from libs.sprite_image.fields import SpriteImageField


class FaqConfig(SingletonModel, StdPage):
    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('faq:index')

    def __str__(self):
        return ugettext("FAQ's")


class Faq(models.Model):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)

    text = CKEditorUploadField(_('text'), blank=True)
    text_second = CKEditorUploadField(_('Content second block'), blank=True)

    ICONS = (
        ('overlay-contract', (-0, -330)),
        ('overlay-insurance', (-45, -330)),
        ('overlay-warranty', (-90, -330)),
        ('overlay-materials', (-135, -330)),
        ('overlay-inspection', (-180, -330)),
    )
    icon = SpriteImageField(_('icon'),
                            sprite='img/sprite.svg',
                            size=(44, 44),
                            choices=ICONS,
                            default=ICONS[0][0],
                            )

    visible = models.BooleanField(_('visible'), default=True)
    sort_order = models.PositiveIntegerField(_('order'), default=0)
    updated = models.DateTimeField(_('change date'), auto_now=True)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ('sort_order',)

    def get_absolute_url(self):
        return resolve_url('faq:detail', slug=self.slug)

    def __str__(self):
        return self.title


class FaqBlock(AttachableBlock):
    BLOCK_VIEW = 'faq.views.faq_block_render'
    header = models.CharField(_('header'), max_length=128, blank=True)

    class Meta:
        verbose_name = _('FAQ block')
        verbose_name_plural = _('FAQs block')
