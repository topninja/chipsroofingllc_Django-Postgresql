from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .base import CampaignAdmin
from ..models import RegularCampaign


@admin.register(RegularCampaign)
class RegularCampaignAdmin(CampaignAdmin):
    custom_fieldsets = (
        (_('Content'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'text',
            )
        }),
    )
