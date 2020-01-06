from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from seo.admin import SeoModelAdminMixin
from attachable_blocks.admin import AttachedBlocksStackedInline
from .models import AboutPageConfig
from apps.std_page.admin import StdPageAdmin


class AboutPageBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки """
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(AboutPageConfig)
class AboutPageConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = StdPageAdmin.fieldsets
    inlines = (AboutPageBlocksInline,)
    suit_form_tabs = (
        ('general', _('General')),
        ('blocks', _('Blocks')),
    )

