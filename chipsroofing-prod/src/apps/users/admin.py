from django.contrib import admin
from django.shortcuts import resolve_url
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin, GroupAdmin as DefaultGroupAdmin
from project.admin import ModelAdminMixin
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """ Форма создания пользователя """
    class Meta:
        model = CustomUser
        fields = ("username",)


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdminMixin, UserAdmin):
    """ Пользователь """
    model = CustomUser
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {
            'fields': ('username', 'password'),
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'avatar'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined')
    list_display = ('avatar_username', 'email', 'first_name', 'last_name', 'is_staff', 'login_as')

    def avatar_username(self, obj):
        return '<img src="{0}" width="20" height="20" style="margin-right: 10px;">{1}'.format(
            obj.micro_avatar,
            obj.username
        )
    avatar_username.short_description = _('username')
    avatar_username.admin_order_field = 'username'
    avatar_username.allow_tags = True

    def get_list_display(self, request):
        """ Login as только для суперюзеров """
        default = super().get_list_display(request)
        if not request.user.is_superuser:
            default = list(default)
            default.remove('login_as')
            return tuple(default)

        return default

    def get_fieldsets(self, request, obj=None):
        """ Запрещаем не-суперюзеру создавать админов """
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            fields_to_remove = ('is_superuser', 'user_permissions')
            for key, opts in fieldsets:
                opts['fields'] = tuple(
                    fieldname
                    for fieldname in opts.get('fields', [])
                    if fieldname not in fields_to_remove
                )

        return fieldsets

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.exclude(is_superuser=True)
        else:
            return qs

    def login_as(self, obj):
        url = resolve_url('admin_users:login_as', user_id=obj.pk)
        caption = _('Login as %(username)s') % {'username': obj.username}
        return '<a href="{0}" class="btn btn-success btn-mini" target="_blank">{1}</a>'.format(url, caption)
    login_as.short_description = _('Login as')
    login_as.allow_tags = True


class GroupAdmin(ModelAdminMixin, DefaultGroupAdmin):
    pass


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
