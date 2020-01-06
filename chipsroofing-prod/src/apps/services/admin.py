from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from seo.admin import SeoModelAdminMixin
from .models import ServicesConfig, Service, ServicesBlock
from attachable_blocks.admin import AttachedBlocksStackedInline, AttachableBlockAdmin
from apps.std_page.admin import StdPageAdmin
from libs.mptt import *


class ServicePageBlocksInline(AttachedBlocksStackedInline):
    verbose_name_plural = _('Page blocks')
    suit_classes = 'suit-tab suit-tab-blocks'


class ServicePageBlocksInlineSecond(AttachedBlocksStackedInline):
    verbose_name_plural = _('Services block')
    set_name = 'service'
    suit_classes = 'suit-tab suit-tab-blocks'


class ServicesBlocksInline(AttachedBlocksStackedInline):
    verbose_name_plural = _('Page blocks')
    suit_classes = 'suit-tab suit-tab-blocks'


class ServicesBlocksInlineSecond(AttachedBlocksStackedInline):
    set_name = 'services'
    verbose_name_plural = _('Services block')
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(ServicesConfig)
class ServicesConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    fieldsets = StdPageAdmin.fieldsets
    inlines = (ServicePageBlocksInlineSecond, ServicePageBlocksInline)
    suit_form_tabs = (
        ('general', _('General')),
        ('content', _('Content second')),
        ('blocks', _('Blocks')),
    )


@admin.register(Service)
class ServiceAdmin(SeoModelAdminMixin, SortableMPTTModelAdmin):
    fieldsets = (
        ('Preview block', {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'background', 'background_alt', 'title', 'slug', 'title_for_seo', 'description', 'parent', 'button_position',
                ('icon', 'visible'),
            ),
        }),
        ('Page content', {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'text',
            ),
        }),
        ('Main popup image', {
            'classes': ('suit-tab', 'suit-tab-popup'),
            'fields': (
                'popup_image',
            ),
        }),
        ('Content second', {
            'classes': ('suit-tab', 'suit-tab-content'),
            'fields': (
                'text_second',
            ),

        }),
    )
    inlines = (ServicesBlocksInlineSecond, ServicesBlocksInline,)
    list_display = ('__str__', 'button_position', 'visible',)
    actions = ('make_visible', 'make_hidden')
    search_fields = ('title',)
    sortable = 'sort_order'
    prepopulated_fields = {
        'slug': ('title',),
    }
    mptt_level_indent = 20
    mptt_indent_field = '__str__'
    suit_form_tabs = (
        ('general', _('General')),
        ('content', _('Content second')),
        ('popup', _('Main popup')),
        ('blocks', _('Blocks')),

    )

    def make_visible(self, request, queryset):
        queryset.update(visible=True)

    make_visible.short_description = _('Make visible')

    def make_hidden(self, request, queryset):
        queryset.update(visible=False)

    make_hidden.short_description = _('Make hidden')


@admin.register(ServicesBlock)
class ServiceBlockAdmin(AttachableBlockAdmin):
    fieldsets = AttachableBlockAdmin.fieldsets + (
        (_('Private'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header', 'image'
            ),
        }),
    )
    suit_form_tabs = (
        ('general', _('General')),
    )
