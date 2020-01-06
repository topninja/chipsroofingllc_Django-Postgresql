from django.conf import settings
from django.contrib import admin
from django.utils import dateformat
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from attachable_blocks.admin import AttachableBlockAdmin, AttachedBlocksStackedInline
from seo.admin import SeoModelAdminMixin
from libs.description import description
from .models import (
    ContactsConfig, Address,
    NotificationReceiver, ContactBlock, Message
)


class ContactsConfigBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки """
    suit_classes = 'suit-tab suit-tab-blocks'


class NotificationReceiverAdmin(ModelAdminInlineMixin, admin.TabularInline):
    """ Получатели сообщений """
    model = NotificationReceiver
    extra = 0
    min_num = 1
    suit_classes = 'suit-tab suit-tab-notify'


@admin.register(Address)
class AddressAdmin(ModelAdminMixin, SingletonModelAdmin):
    """ Адрес """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'address', 'city', 'region', 'zip', 'url', 'phone','fax','email', 'coords',
            ),
        }),
    )
    list_display = ('city', 'address',)
    sortable = 'sort_order'
    suit_form_tabs = (
        ('general', _('General')),
        ('phones', _('Phones')),
    )

    class Media:
        js = (
            'contacts/admin/js/coords.js',
        )


@admin.register(ContactsConfig)
class ContactsConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header', 'license'
            ),
        }),
    )
    inlines = (NotificationReceiverAdmin, ContactsConfigBlocksInline)
    suit_form_tabs = (
        ('general', _('General')),
        ('notify', _('Notifications')),
        ('blocks', _('Blocks')),
    )


@admin.register(Message)
class MessageAdmin(ModelAdminMixin, admin.ModelAdmin):
    """ Сообщение """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'type_message', 'name', 'phone', 'email',
            ),
        }),
        (_('Text'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'message',
            ),
        }),
        (_('Info'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'date_fmt', 'referer',
            ),
        }),
    )
    search_fields = ('name', 'email')
    list_filter = ('type_message',)
    readonly_fields = ('type_message', 'name', 'phone', 'email', 'message', 'date_fmt', 'referer')
    list_display = ('type_message', 'name', 'email', 'phone', 'message_fmt', 'date_fmt')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def message_fmt(self, obj):
        return description(obj.message, 60, 80)

    message_fmt.short_description = _('Message')
    message_fmt.admin_order_field = 'message'

    def date_fmt(self, obj):
        return dateformat.format(localtime(obj.date), settings.DATETIME_FORMAT)

    date_fmt.short_description = _('Date')
    date_fmt.admin_order_field = 'date'


@admin.register(ContactBlock)
class ContactBlockAdmin(AttachableBlockAdmin):
    """ Подключаемый блок с контактной формой """
    fieldsets = AttachableBlockAdmin.fieldsets + (
        (_('Customization'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('header', 'description'),
        }),
    )
