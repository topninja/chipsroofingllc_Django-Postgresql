from django import forms
from django.contrib import admin
from django.conf import settings
from django.shortcuts import resolve_url
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from project.admin import ModelAdminMixin
from project.admin.widgets import LinkWidget
from .models import LogEntry


ACTION_CHOICES = (
    (ADDITION, _('Addition')),
    (CHANGE, _('Change')),
    (DELETION, _('Deletion')),
)


class LogEntryAdminForm(forms.ModelForm):
    object_link = forms.Field(
        required=False,
        label=_('Entry'),
        widget=LinkWidget,
    )

    user_link = forms.Field(
        required=False,
        label=_('User'),
        widget=LinkWidget,
    )

    class Meta:
        model = LogEntry
        fields = '__all__'
        widgets = {
            'action_flag': forms.Select(choices=ACTION_CHOICES),
            'change_message': forms.Textarea(attrs={'class': 'input-block-level', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            obj = self.instance.get_edited_object()
        except ObjectDoesNotExist:
            self.fields['object_link'].widget = forms.HiddenInput()
            self.fields['object_link'].help_text = '--//--'
        else:
            self.initial['object_link'] = self.instance.get_admin_url()
            self.fields['object_link'].widget.text = str(obj)

        if self.instance.user:
            admin_user_model = settings.AUTH_USER_MODEL.lower().replace('.', '_')
            self.initial['user_link'] = resolve_url('admin:{}_change'.format(admin_user_model), self.instance.user.pk)
            self.fields['user_link'].widget.text = str(self.instance.user)
        else:
            self.fields['user_link'].widget = forms.HiddenInput()
            self.fields['user_link'].help_text = '--//--'


class LogEntryActionFilter(SimpleListFilter):
    title = _('Action type')
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        return ACTION_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(action_flag=value)
        else:
            return queryset


@admin.register(LogEntry)
class LogEntryAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = LogEntryAdminForm
    change_form_template = 'admin_log/admin/change_form.html'
    list_display = ('__str__', 'user_link', 'action_type', 'action_time')
    list_filter = ('user', LogEntryActionFilter, 'action_time',)
    readonly_fields = (
        'action_type', 'change_message', 'action_time',
    )
    fieldsets = (
        (_('Entry'), {
            'fields': ('object_link', 'user_link', ),
        }),
        (_('Action'), {
            'fields': ('action_type', 'change_message', 'action_time', ),
        }),
    )

    def user_link(self, obj):
        admin_user_model = settings.AUTH_USER_MODEL.lower().replace('.', '_')
        return '<a href="%s" target="_blank">%s</a>' % (
            resolve_url('admin:{}_change'.format(admin_user_model), obj.user.pk),
            obj.user.username
        )
    user_link.short_description = _('User')
    user_link.allow_tags = True

    def action_type(self, obj):
        return dict(ACTION_CHOICES).get(obj.action_flag)
    action_type.short_description = _('Action type')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return ()
