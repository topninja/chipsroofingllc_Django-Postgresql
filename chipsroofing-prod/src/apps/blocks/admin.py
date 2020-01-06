from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableStackedInline, SortableTabularInline
from attachable_blocks.admin import AttachableBlockAdmin
from project.admin.base import ModelAdminInlineMixin
from .models import (
    Estimate, EstimateBlock, Partners, PartnersBlock,
    Video, VideosBlock)


class EstimateInline(ModelAdminInlineMixin, SortableTabularInline):
    model = Estimate
    extra = 0
    min_num = 4
    max_num = 4
    sortable = 'sort_order'
    suit_classes = 'suit-tab suit-tab-estimate'


@admin.register(EstimateBlock)
class EstimateBlockAdmin(AttachableBlockAdmin):
    fieldsets = AttachableBlockAdmin.fieldsets + (
        (_('Private'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header', ('description', 'image')
            ),
        }),
    )
    inlines = (EstimateInline,)
    suit_form_tabs = (
        ('general', _('General')),
        ('estimate', _('estimate')),
    )


class PartnersInline(ModelAdminInlineMixin, SortableTabularInline):
    model = Partners
    extra = 0
    min_num = 3
    sortable = 'sort_order'
    suit_classes = 'suit-tab suit-tab-general'


@admin.register(PartnersBlock)
class PartnersBlockAdmin(AttachableBlockAdmin):
    fieldsets = AttachableBlockAdmin.fieldsets + (
        (_('Private'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header',
            ),
        }),
    )
    inlines = (PartnersInline,)
    suit_form_tabs = (
        ('general', _('General')),
    )


class VideoInline(ModelAdminInlineMixin, SortableStackedInline):
    model = Video
    extra = 0
    sortable = 'sort_order'
    suit_classes = 'suit-tab suit-tab-general'


@admin.register(VideosBlock)
class VideosBlockAdmin(AttachableBlockAdmin):
    fieldsets = AttachableBlockAdmin.fieldsets + (
        (_('Private'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'video_title',
            ),
        }),
    )
    inlines = (VideoInline,)
