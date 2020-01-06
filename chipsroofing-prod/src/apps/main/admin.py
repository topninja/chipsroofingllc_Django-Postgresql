from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from seo.admin import SeoModelAdminMixin
from attachable_blocks.admin import AttachedBlocksStackedInline
from .models import MainPageConfig


class MainPageBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки """
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(MainPageConfig)
class MainPageConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = (
        ('Main page config', {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title', 'description',
            ),
        }),
    )
    inlines = (MainPageBlocksInline,)
    suit_form_tabs = (
        ('general', _('General')),
        ('blocks', _('Blocks')),
    )
