from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatechars
from project.admin import ModelAdminMixin
from .models import Log


@admin.register(Log)
class LogAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'status', 'msg_body', 'inv_id', 'created',
            ),
        }),
        (_('Request'), {
            'fields': (
                'fmt_request_get', 'fmt_request_post', 'request_ip',
            ),
        }),
    )
    list_filter = ('status',)
    search_fields = ('inv_id', 'request_ip')
    list_display = ('status', 'short_msg_body', 'inv_id', 'request_ip', 'created')
    readonly_fields = (
        'inv_id', 'status', 'msg_body',
        'fmt_request_get', 'fmt_request_post', 'request_ip',
        'created',
    )
    list_display_links = ('status', 'short_msg_body')
    date_hierarchy = 'created'

    def short_msg_body(self, obj):
        return truncatechars(obj.msg_body, 48)
    short_msg_body.short_description = _('Message')

    def fmt_request_get(self, obj):
        return obj.request_get.replace('&', '\n')
    fmt_request_get.short_description = _('GET')

    def fmt_request_post(self, obj):
        return obj.request_post.replace('&', '\n')
    fmt_request_post.short_description = _('POST')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
