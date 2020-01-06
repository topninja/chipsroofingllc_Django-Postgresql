from django.db import models
from libs.sprite_image.fields import SpriteImageField
from attachable_blocks.models import AttachableBlock
from django.utils.translation import ugettext_lazy as _, ugettext
from libs.storages.media_storage import MediaStorage
from django.contrib.contenttypes.models import ContentType
from libs.file_field.fields import ImageField
from gallery.models import GalleryBase, GalleryImageItem
from libs.stdimage.fields import StdImageField
from libs.videolink_field.fields import VideoLinkField
from ckeditor.fields import CKEditorUploadField


class EstimateBlock(AttachableBlock):
    """ Подключаемый блок с контактной формой """
    BLOCK_VIEW = 'blocks.views.estimate_block_render'

    header = models.CharField(_('header'), max_length=128, blank=True)
    description = models.TextField(_('description'), blank=True)
    image = StdImageField(_('background'),
                          storage=MediaStorage('blocks/estimate'),
                          min_dimensions=(450, 0),
                          admin_variation='admin',
                          crop_area=True,
                          null=True,
                          blank=True,
                          variations=dict(
                              normal=dict(
                                  size=(1090, 380),
                                  crop=True
                              ),
                              tablet=dict(
                                  size=(600, 0),
                                  crop=False
                              ),
                              mobile=dict(
                                  size=(290, 376),
                                  crop=False
                              ),
                              admin=dict(
                                  size=(300, 200),
                                  crop=True
                              ),
                          ),
                          )

    class Meta:
        verbose_name = _('Estimate block')
        verbose_name_plural = _('Estimate blocks')


class Estimate(models.Model):
    config = models.ForeignKey(EstimateBlock, related_name='estimate', default=True)
    ICONS = (
        ('icon-1', (0, -380)),
        ('icon-2', (-34, -380)),
        ('icon-3', (-68, -380)),
        ('icon-4', (-102, -380)),
    )
    icon = SpriteImageField(_('icon'),
                            sprite='img/sprite.svg',
                            size=(34, 34),
                            choices=ICONS,
                            default=ICONS[0][0],
                            background='#0080b0',
                            )
    title = models.CharField(_('title'), max_length=128, blank=True)

    sort_order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _("Free Estimate")
        verbose_name_plural = _('Free Estimate')

    def __str__(self):
        return self.title


class PartnersBlock(AttachableBlock):
    BLOCK_VIEW = 'blocks.views.partners_block_render'

    header = models.CharField(_('header'), max_length=128, blank=True)

    class Meta:
        verbose_name = _('Partners block')
        verbose_name_plural = _('Partners blocks')


class Partners(models.Model):
    config = models.ForeignKey(PartnersBlock, related_name='partners', default=True)
    image = ImageField(_('image'), storage=MediaStorage('blocks/partners'))
    sort_order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _("Partners & Affiliations")
        verbose_name_plural = _('Partners & Affiliations')

    def __str__(self):
        return ugettext('Partners')


class VideosBlock(AttachableBlock):
    BLOCK_VIEW = 'blocks.views.videos_render'
    video_title = models.CharField(_('header'), max_length=255)

    class Meta:
        verbose_name = _('Video content block')
        verbose_name_plural = _('Video content block')


class Video(models.Model):
    config = models.OneToOneField(VideosBlock, related_name='videos')

    video = VideoLinkField(_('video'), providers=('youtube',), blank=True)
    video_webm = models.FileField(_('video WebM'), storage=MediaStorage('main/video'), blank=True)
    video_mp4 = models.FileField(_('video MP4'), storage=MediaStorage('main/video'), blank=True)

    content = CKEditorUploadField(_('video and content'), blank=True)

    sort_order = models.IntegerField(_('order'), default=0)

    class Meta:
        ordering = ('sort_order',)
        verbose_name = _('video')
        verbose_name_plural = _('videos')

    def __str__(self):
        return ugettext('Video')
