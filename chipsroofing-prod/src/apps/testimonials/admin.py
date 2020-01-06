from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from seo.admin import SeoModelAdminMixin
from attachable_blocks.admin import AttachedBlocksStackedInline
from .models import TestimonialsPageConfig, Testimonials
from project.admin.base import ModelAdminMixin
from suit.admin import SortableModelAdmin
from apps.std_page.admin import StdPageAdmin
from .models import TestimonialsBlock
from attachable_blocks.admin import AttachableBlockAdmin


class TestimonialsPageBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки """
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(TestimonialsPageConfig)
class TestimonialsPageConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = StdPageAdmin.fieldsets
    inlines = (TestimonialsPageBlocksInline,)
    suit_form_tabs = (
        ('general', _('General')),
        ('content', _('Content second')),
        ('testimonials', _('Testimonials')),
        ('blocks', _('Blocks')),
    )


@admin.register(Testimonials)
class TestimonialAdmin(ModelAdminMixin, SortableModelAdmin):
    fieldsets = (
        ('Page content', {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title', 'description', 'star', 'visible',
            ),
        }),
    )
    sortable = 'sort_order'
    actions = ('make_visible', 'make_hidden')
    list_display = ('__str__', 'visible')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def make_visible(self, request, queryset):
        queryset.update(visible=True)

    make_visible.short_description = _('Make visible')

    def make_hidden(self, request, queryset):
        queryset.update(visible=False)

    make_hidden.short_description = _('Make hidden')


@admin.register(TestimonialsBlock)
class TestimonialsBlockAdmin(AttachableBlockAdmin):
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
