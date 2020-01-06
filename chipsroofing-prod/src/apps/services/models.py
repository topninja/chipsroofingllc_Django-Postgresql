from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _, ugettext
from solo.models import SingletonModel
from libs.autoslug import AutoSlugField
from apps.std_page.models import StdPage
from libs.sprite_image.fields import SpriteImageField
from attachable_blocks.models import AttachableBlock
from libs.storages.media_storage import MediaStorage
from libs.stdimage.fields import StdImageField
from mptt.models import MPTTModel, TreeForeignKey


class ServicesConfig(SingletonModel, StdPage):
    class Meta:
        verbose_name = _('settings')

    def get_absolute_url(self):
        return resolve_url('services:index')

    def __str__(self):
        return ugettext('SERVICES')


class Service(MPTTModel, StdPage):
    title_for_seo = models.CharField(_('title for SEO'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title', unique=True)

    CHOICES = (
        ('top-left', 'Top left'),
        ('top-middle', 'Top middle'),
        ('top-right', 'Top right'),
        ('bottom-left', 'Bottom left'),
        ('bottom-middle', 'Bottom middle'),
        ('bottom-right', 'Bottom right'),
    )

    button_position = models.CharField(_('Button position'), max_length=64, choices=CHOICES, null=True, blank=True, unique=True)

    ICONS = (
        ('overlay-newroof', (-0, -232)),
        ('overlay-comerc-roof', (-45, -232)),
        ('overlay-resident-roof', (-93, -232)),
        ('overlay-roof-rep', (-138, -232)),
        ('overlay-siding', (-183, -232)),
        ('overlay-gutter', (-228, -232)),
    )
    icon = SpriteImageField(_('icon'),
                            sprite='img/sprite.svg',
                            size=(44, 44),
                            choices=ICONS,
                            default=ICONS[0][0],
                            )

    visible = models.BooleanField(_('visible'), default=True)
    popup_image = StdImageField(_('Main popup image'),
                                storage=MediaStorage('services_popup/img'),
                                min_dimensions=(450, 0),
                                admin_variation='admin',
                                crop_area=True,
                                null=True,
                                blank=True,
                                variations=dict(
                                    wide=dict(
                                        size=(1920, 1720),
                                        stretch=True,
                                    ),
                                    desktop=dict(
                                        size=(1400, 1250),
                                    ),
                                    mobile=dict(
                                        size=(800, 750),
                                    ),
                                    micro=dict(
                                        size=(480, 430),
                                    ),
                                    admin=dict(
                                        size=(640, 480),
                                        crop=True
                                    ),
                                ),
                                )
    parent = TreeForeignKey('self',
                            blank=True,
                            null=True,
                            verbose_name=_('parent service'),
                            related_name='children',
                            limit_choices_to={
                                'parent': None
                            }
                            )

    class MPTTMeta:
        order_insertion_by = ('sort_order',)

    sort_order = models.PositiveIntegerField(_('order'), default=0)


    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ('sort_order',)

    def get_absolute_url(self):
        if self.parent:
            return resolve_url('services:sub_detail', parent_slug=self.parent.slug, slug=self.slug)
        else:
            return resolve_url('services:detail', slug=self.slug)

    def __str__(self):
        return self.title


class ServicesBlock(AttachableBlock):
    BLOCK_VIEW = 'services.views.services_block_render'
    header = models.CharField(_('header'), max_length=128, blank=True)
    image = StdImageField(_('Header image'),
                          storage=MediaStorage('services_block/img'),
                          min_dimensions=(450, 0),
                          admin_variation='admin',
                          crop_area=True,
                          null=True,
                          blank=True,
                          variations=dict(
                              normal=dict(
                                  size=(480, 300),
                                  crop=True
                              ),
                              tablet=dict(
                                  size=(480, 0),
                                  crop=False
                              ),
                              admin=dict(
                                  size=(300, 150),
                                  crop=True
                              ),
                          ),
                          )

    class Meta:
        verbose_name = _('Services block')
        verbose_name_plural = _('Services block')
