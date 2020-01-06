from django.utils.translation import ugettext_lazy as _
from attachable_blocks.admin import AttachedBlocksStackedInline
from seo.admin import SeoModelAdminMixin


class PageBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки """
    suit_classes = 'suit-tab suit-tab-blocks'


class StdPageAdmin(SeoModelAdminMixin):
    fieldsets = (
        ('Page content', {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'background', 'background_alt', 'title', 'description', 'text'
            ),

        }),
        ('Content second', {
            'classes': ('suit-tab', 'suit-tab-content'),
            'fields': (
                'text_second',
            ),

        }),
    )
    inlines = (PageBlocksInline,)
    suit_form_tabs = (
        ('general', _('General')),
        ('content', _('Content second')),
        ('blocks', _('Blocks')),
    )
