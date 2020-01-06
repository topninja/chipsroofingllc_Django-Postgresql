from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from suit.admin import SortableModelAdmin
from seo.admin import SeoModelAdminMixin
from .models import FaqConfig, Faq, FaqBlock
from attachable_blocks.admin import AttachedBlocksStackedInline, AttachableBlockAdmin
from apps.std_page.admin import StdPageAdmin


class FaqPageBlocksInline(AttachedBlocksStackedInline):
    verbose_name_plural = _('FAQ page blocks')
    suit_classes = 'suit-tab suit-tab-blocks'


class FaqPageBlocksInlineSecond(AttachedBlocksStackedInline):
    set_name = 'question_block'
    verbose_name_plural = _('FAQ question block')
    suit_classes = 'suit-tab suit-tab-blocks'


class FaqBlocksInline(AttachedBlocksStackedInline):
    verbose_name_plural = _('FAQ page blocks')
    suit_classes = 'suit-tab suit-tab-blocks'


class FaqBlocksInlineSecond(AttachedBlocksStackedInline):
    set_name = 'questions_block'
    verbose_name_plural = _('FAQ question block')
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(FaqConfig)
class FaqPageConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = StdPageAdmin.fieldsets
    inlines = (FaqPageBlocksInlineSecond, FaqPageBlocksInline )
    suit_form_tabs = (
        ('general', _('General')),
        ('content', _('Content second')),
        ('blocks', _('Blocks')),
    )


@admin.register(Faq)
class FaqAdmin(SeoModelAdminMixin, SortableModelAdmin):
    fieldsets = (
        ('Preview block', {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title', 'slug', ('icon', 'visible'),
            ),
        }),
        ('Page content', {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'description', 'text',
            ),
        }),
        ('Content second', {
            'classes': ('suit-tab', 'suit-tab-content'),
            'fields': (
                'text_second',
            ),

        }),
    )

    inlines = (FaqBlocksInlineSecond, FaqBlocksInline)
    sortable = 'sort_order'
    prepopulated_fields = {
        'slug': ('title',),
    }
    actions = ('make_visible', 'make_hidden')
    list_display = ('__str__', 'visible')
    suit_form_tabs = (
        ('general', _('General')),
        ('content', _('Content second')),
        ('blocks', _('Blocks')),

    )

    def make_visible(self, request, queryset):
        queryset.update(visible=True)

    make_visible.short_description = _('Make visible')

    def make_hidden(self, request, queryset):
        queryset.update(visible=False)

    make_hidden.short_description = _('Make hidden')


@admin.register(FaqBlock)
class FaqBlockAdmin(AttachableBlockAdmin):
    fieldsets = AttachableBlockAdmin.fieldsets + (
        (_('Private'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header',
            ),
        }),
    )
    suit_form_tabs = (
        ('general', _('General')),
    )
