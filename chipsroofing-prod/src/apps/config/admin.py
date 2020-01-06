from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin.base import ModelAdminMixin
from .models import Config


@admin.register(Config)
class ConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (

            ),
        }),
    )
    suit_form_tabs = (
        ('general', _('General')),
    )
