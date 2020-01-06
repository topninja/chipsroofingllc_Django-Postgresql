from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from seo.admin import SeoModelAdminMixin
from attachable_blocks.admin import AttachedBlocksStackedInline
from apps.std_page.admin import StdPageAdmin
from .models import ExamplesPageConfig, ExamplesBlock
from attachable_blocks.admin import AttachableBlockAdmin


class ExamplesPageBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки """
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(ExamplesPageConfig)
class ExamplesPageConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = StdPageAdmin.fieldsets + (
        ('Work examples', {
            'classes': ('suit-tab', 'suit-tab-examples'),
            'fields': (
                'gallery',
            ),
        }),
    )
    inlines = (ExamplesPageBlocksInline,)
    suit_form_tabs = (
        ('general', _('General')),
        ('content', _('Content second')),
        ('examples', _('Examples')),
        ('blocks', _('Blocks')),
    )


@admin.register(ExamplesBlock)
class ExamplesBlockAdmin(AttachableBlockAdmin):
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
