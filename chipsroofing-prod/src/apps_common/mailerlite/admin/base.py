import io
import csv
from itertools import islice
from django import forms
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.db import transaction
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, Http404
from django.contrib.messages import add_message, SUCCESS
from django.utils.translation import ugettext_lazy as _, ungettext_lazy, get_language
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from project.admin.filters import HierarchyFilter
from libs.admin_utils import get_change_url
from libs.cookies import set_cookie
from libs.description import description
from libs.download import AttachmentResponse
from libs.autocomplete.filters import AutocompleteListFilter
from libs.autocomplete.widgets import AutocompleteMultipleWidget
from libs.upload import upload_chunked_file, TemporaryFileNotFoundError, NotLastChunk
from ..models import MailerConfig, Group, Subscriber
from ..utils import fill_demo, make_subscriber
from .. import api


class StatusFilter(HierarchyFilter):
    title = _('Status')
    parameter_name = 'status'
    default_value = 'all'

    def __init__(self, request, params, model, model_admin):
        self._choices = [
            ('all', _('All')),
        ]
        self._choices.extend(model.STATUS_CHOICES)
        super().__init__(request, params, model, model_admin)

    def lookups(self, request, model_admin):
        result = []
        for key, name in self._choices:
            qs = self.queryset(
                request,
                queryset=model_admin.model._default_manager,
                value=key
            )
            result.append((key, '%s (%d)' % (name, qs.count())))
        return result

    def get_branch_choices(self, value):
        return [
            (value, dict(self._choices).get(value))
        ]

    def queryset(self, request, queryset, value=None):
        value = value or self.value()
        if value == 'all':
            return queryset
        if value is not None:
            queryset = queryset.filter(status=value)
        return queryset


class MailerConfigForm(forms.ModelForm):
    class Meta:
        model = MailerConfig
        fields = '__all__'
        widgets = {
            'from_name': forms.TextInput(
                attrs={
                    'class': 'input-xlarge',
                }
            ),
            'company': forms.TextInput(
                attrs={
                    'class': 'input-xlarge',
                }
            ),
        }


@admin.register(MailerConfig)
class MailerConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (_('Default sender'), {
            'fields': (
                'from_name', 'from_email',
            ),
        }),
        (_('Email style'), {
            'fields': (
                'bg_color', 'bg_image',
            ),
        }),
        (_('Email footer'), {
            'fields': (
                'footer_text', 'website', 'contact_email',
            ),
        }),
    )
    form = MailerConfigForm


@admin.register(Group)
class GroupAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_form_template = 'mailerlite/admin/change_form_group.html'

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'name', 'subscribable',
            )
        }),
        (_('Subscribers'), {
            'classes': ('suit-tab', 'suit-tab-statistics'),
            'fields': (
                'total', 'active', 'bounced', 'unsubscribed',
            )
        }),
        (_('Emails'), {
            'classes': ('suit-tab', 'suit-tab-statistics'),
            'fields': (
                'sent', 'opened', 'clicked',
            )
        }),
        (_('Dates'), {
            'classes': ('suit-tab', 'suit-tab-statistics'),
            'fields': (
                'date_created', 'date_updated',
            )
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-debug'),
            'fields': (
                'remote_id',
            )
        }),
    )
    readonly_fields = (
        'total', 'active', 'bounced', 'unsubscribed',
        'sent', 'opened', 'clicked',
        'date_created', 'date_updated',
    )
    list_display = (
        'view', 'download', 'upload',
        'name', 'active', 'unsubscribed', 'sent', 'opened', 'clicked',
        'subscribable', 'is_synced',
    )
    list_display_links = ('name', )

    class Media:
        js = (
            'common/js/plupload/plupload.full.min.js',
            'common/js/plupload/i18n/%s.js' % (get_language(),),
            'common/js/uploader.js',
            'mailerlite/admin/js/upload_csv.js',
        )
        css = {
            'all': (
                'mailerlite/admin/css/upload_csv.css',
            )
        }

    def get_suit_form_tabs(self, request, add=False):
        if request.user.is_superuser:
            return (
                ('general', _('General')),
                ('statistics', _('Statistics')),
                ('debug', _('Debugging')),
            )
        else:
            return (
                ('general', _('General')),
                ('statistics', _('Statistics')),
            )

    def has_add_permission(self, request):
        """ Право на добавление суперюзеру """
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """ Право на удаление суперюзеру """
        return request.user.is_superuser

    def suit_cell_attributes(self, obj, column):
        default = super().suit_cell_attributes(obj, column)
        if column in ('download', 'upload'):
            default.update({
                'class': 'mini-column'
            })
        return default

    def view(self, obj):
        return ('<a href="{href}" title="{title}">'
                '   <span class="icon-list icon-alpha75"></span>'
                '</a>').format(
            href=reverse('admin:%s_subscriber_changelist' % self.model._meta.app_label) + '?group=%d' % obj.pk,
            title=_('Show subscribers')
        )
    view.short_description = '#'
    view.allow_tags = True

    def is_synced(self, obj):
        return not obj.need_export
    is_synced.short_description = _('Synchronized')
    is_synced.admin_order_field = 'need_export'
    is_synced.boolean = True

    def upload(self, obj):
        return ('<a href="{url}" title="{title}" class="upload-csv" data-reload="1">'
                '   <span class="icon-upload icon-alpha75"></span>'
                '</a>').format(
            title=_('Import subscribers from CSV file'),
            url=reverse('admin:%s_group_upload_csv' % self.model._meta.app_label, kwargs={
                'group_id': obj.pk
            }),
        )
    upload.short_description = '#'
    upload.allow_tags = True

    def download(self, obj):
        return ('<a href="{href}" title="{title}">'
                '   <span class="icon-download icon-alpha75"></span>'
                '</a>').format(
            href=reverse('admin:%s_group_download_csv' % self.model._meta.app_label, kwargs={
                'group_id': obj.pk
            }),
            title=_('Export subscribers as a CSV file'),
        )
    download.short_description = '#'
    download.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        csv_urls = [
            url(
                r'^upload_csv/(?P<group_id>\d+)/$',
                self.admin_site.admin_view(self.upload_csv),
                name='%s_%s_upload_csv' % info
            ),
            url(
                r'^download_csv/(?P<group_id>\d+)/$',
                self.admin_site.admin_view(self.download_csv),
                name='%s_%s_download_csv' % info
            ),
        ]
        return csv_urls + urls

    @staticmethod
    def download_csv(request, group_id):
        # Поиск списка подписчиков
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            raise Http404

        class Echo(object):
            def write(self, value):
                return value

        pseudo_buffer = Echo()
        csv_writer = csv.writer(pseudo_buffer)
        stream = (
            csv_writer.writerow([
                subscriber['email'],
                subscriber['name'],
                subscriber['last_name'],
                subscriber['company'],
                subscriber['status'],
            ])
            for subscriber in Subscriber.objects.filter(
                groups=group,
            ).order_by('email').distinct('email').values()
        )
        return AttachmentResponse(request, stream, filename='%s.csv' % group.name)

    @staticmethod
    def upload_csv(request, group_id):
        try:
            csvfile = upload_chunked_file(request, 'csv')
        except TemporaryFileNotFoundError as e:
            return JsonResponse({
                'message': str(e),
            }, status=400)
        except NotLastChunk:
            return JsonResponse({})

        # Поиск списка подписчиков
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return JsonResponse({
                'message': _('There are no such list'),
            }, status=400)

        added_count = 0
        csv_reader = csv.reader(io.TextIOWrapper(csvfile.file))
        while True:
            data = tuple(
                dict(zip(('email', 'name', 'last_name', 'company', 'status'), row))
                for row in islice(csv_reader, 100)
            )
            if not data:
                break

            with transaction.atomic():
                for record in data:
                    if not record['email']:
                        continue

                    subscriber = make_subscriber(**record)
                    if not subscriber.groups.filter(pk=group.pk).exists():
                        subscriber.groups.add(group)
                        added_count += 1

        csvfile.close()
        add_message(request, SUCCESS,
            ungettext_lazy(
                'Successfully added %d subscriber.',
                'Successfully added %d subscribers.',
                number=added_count
            ) % added_count
        )
        return JsonResponse({
            'redirect': reverse('admin:%s_subscriber_changelist' % Group._meta.app_label) + '?group=%d' % group.pk,
        })


class CampaignForm(forms.ModelForm):
    class Meta:
        widgets = {
            'from_name': forms.TextInput(
                attrs={
                    'class': 'input-xlarge',
                }
            ),
            'groups': AutocompleteMultipleWidget(
                expressions='name__icontains',
                attrs={
                    'style': 'width: 600px',
                }
            ),
        }


class CampaignAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_form_template = 'mailerlite/admin/change_form_campaign.html'

    custom_fieldsets = ()
    form = CampaignForm
    readonly_fields = (
        'total_recipients', 'opened', 'clicked',
        'date_created', 'date_send',
        'created', 'modified',
    )
    list_filter = (StatusFilter, )
    list_display = (
        'view', 'short_subject', 'recipients',
        'total_recipients', 'opened', 'clicked', 'status_box',
        'is_synced', 'date_created',
    )
    list_display_links = ('short_subject', )

    class Media:
        js = (
            'mailerlite/admin/js/sendtest.js',
        )
        css = {
            'all': (
                'mailerlite/admin/css/sendtest.css',
            )
        }

    def get_suit_form_tabs(self, request, add=False):
        if request.user.is_superuser:
            return (
                ('general', _('General')),
                ('statistics', _('Statistics')),
                ('debug', _('Debugging')),
            )
        else:
            return (
                ('general', _('General')),
                ('statistics', _('Statistics')),
            )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        form.current_user = request.user
        return form

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                'classes': ('suit-tab', 'suit-tab-general'),
                'fields': (
                    'subject', 'from_name', 'from_email', 'groups',
                )
            }),
        ) + self.custom_fieldsets + (
            (_('Emails'), {
                'classes': ('suit-tab', 'suit-tab-statistics'),
                'fields': (
                    'total_recipients', 'opened', 'clicked',
                )
            }),
            (_('Dates'), {
                'classes': ('suit-tab', 'suit-tab-statistics'),
                'fields': (
                    'date_created', 'date_send',
                )
            }),
            (None, {
                'classes': ('suit-tab', 'suit-tab-debug'),
                'fields': (
                    'status', 'export_allowed', 'remote_id',
                )
            }),
        )

    def has_delete_permission(self, request, obj=None):
        """ Право на удаление """
        if request.user.is_superuser:
            return True
        default = super().has_delete_permission(request, obj)
        if obj is None:
            return default
        return not obj.export_allowed

    def get_actions(self, request):
        """ Массовое удаление только для суперюзера """
        default = super().get_actions(request)
        if not request.user.is_superuser and 'delete_selected' in default:
            del default['delete_selected']
        return default

    def get_changeform_initial_data(self, request):
        group = Group.objects.filter(subscribable=True).first()
        if not group:
            group = Group.objects.first()

        config = MailerConfig.get_solo()
        return {
            'from_name': config.from_name,
            'from_email': config.from_email,
            'groups': [group.pk],
        }

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if not add:
            info = self.model._meta.app_label, self.model._meta.model_name
            context.update({
                'sendtest_url': reverse('admin:%s_%s_sendtest' % info, args=(obj.pk,)),
            })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        submit_urls = [
            url(r'^(\d+)/start/$', self.admin_site.admin_view(self.start_campaign), name='%s_%s_start' % info),
            url(r'^(\d+)/cancel/$', self.admin_site.admin_view(self.cancel_campaign), name='%s_%s_cancel' % info),
            url(r'^(\d+)/sendtest/$', self.admin_site.admin_view(self.sendtest), name='%s_%s_sendtest' % info),
        ]
        return submit_urls + urls

    def recipients(self, obj):
        if obj.groups.exists():
            meta = getattr(self.model.groups.field.rel.to, '_meta')
            return ' / '.join(
                '<a href="{0}">{1}</a>'.format(
                    get_change_url(meta.app_label, meta.model_name, group.pk),
                    group
                )
                for group in obj.groups.all()
            )
    recipients.short_description = _('Recipients')
    recipients.allow_tags = True

    def short_subject(self, obj):
        return description(obj.subject, 30, 60)
    short_subject.short_description = _('Subject')
    short_subject.admin_order_field = 'subject'

    def is_synced(self, obj):
        return obj.remote_id != 0
    is_synced.short_description = _('Synchronized')
    is_synced.boolean = True

    def status_box(self, obj):
        status_text = dict(self.model.STATUS_CHOICES).get(obj.status)
        info = self.model._meta.app_label, self.model._meta.model_name
        button_tpl = '<a href="{href}" class="btn btn-mini {classes}" style="margin-left: 5px">{text}</a>'

        if not obj.export_allowed:
            return """
                <nobr>
                    {text}&nbsp;{publish}
                </nobr>
            """.format(
                text=status_text,
                publish=button_tpl.format(
                    href=reverse('admin:%s_%s_start' % info, args=(obj.id,)),
                    classes='btn-success',
                    text=_('Start')
                ),
            )
        elif obj.status == api.campaings.STATUS_DRAFT:
            return """
                <nobr>
                    {text}&nbsp;{action}
                </nobr>
            """.format(
                text=status_text,
                action=button_tpl.format(
                    href=reverse('admin:%s_%s_cancel' % info, args=(obj.id,)),
                    classes='btn-danger',
                    text=_('Cancel')
                ),
            )
        else:
            return status_text
    status_box.short_description = _('Status')
    status_box.admin_order_field = 'status'
    status_box.allow_tags = True

    def start_campaign(self, request, campaign_id):
        try:
            campaign = self.model.objects.get(
                pk=campaign_id,
                status=api.campaings.STATUS_DRAFT,
                export_allowed=False,
            )
        except self.model.DoesNotExist:
            pass
        else:
            campaign.export_allowed = True
            campaign.save()

        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)

    def cancel_campaign(self, request, campaign_id):
        try:
            campaign = self.model.objects.get(
                pk=campaign_id,
                status=api.campaings.STATUS_DRAFT,
                export_allowed=True,
            )
        except self.model.DoesNotExist:
            pass
        else:
            campaign.export_allowed = False
            campaign.save()

        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_changelist' % info)

    def sendtest(self, request, campaign_id):
        from premailer import Premailer
        from django.core.mail import send_mail, BadHeaderError

        receiver = request.POST.get('receiver')
        if not receiver:
            raise Http404

        try:
            campaign = self.model.objects.get(pk=campaign_id)
        except self.model.DoesNotExist:
            pass
        else:
            content = campaign.final_html(request, scheme='http://')
            content = fill_demo(content)
            content = Premailer(content, strip_important=False).transform()

            plain = campaign.render_plain(request)
            plain = fill_demo(plain)

            try:
                send_mail(
                    subject=campaign.test_subject,
                    message=plain,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[receiver],
                    html_message=content,
                )
            except BadHeaderError:
                pass

        response = JsonResponse({})
        set_cookie(response, 'last_receiver', receiver)
        return response


class SubscriberGroupFilter(AutocompleteListFilter):
    model = Group
    multiple = False
    expression = 'name__icontains'

    def filter(self, queryset, value):
        return queryset.filter(groups=value).distinct()


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'
        widgets = {
            'groups': AutocompleteMultipleWidget(
                expressions='name__icontains',
                attrs={
                    'style': 'width: 600px',
                }
            ),
        }


@admin.register(Subscriber)
class SubscriberAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'email', 'groups',
            )
        }),
        (_('Additional information'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'name', 'last_name', 'company',
            )
        }),
        (_('Emails'), {
            'classes': ('suit-tab', 'suit-tab-statistics'),
            'fields': (
                'sent', 'opened', 'clicked',
            )
        }),
        (_('Dates'), {
            'classes': ('suit-tab', 'suit-tab-statistics'),
            'fields': (
                'date_created', 'date_subscribe', 'date_unsubscribe', 'date_updated',
            )
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-debug'),
            'fields': (
                'status', 'remote_id',
            )
        }),
    )
    form = SubscriberForm
    readonly_fields = (
        'sent', 'opened', 'clicked',
        'date_created', 'date_subscribe', 'date_unsubscribe', 'date_updated',
    )
    ordering = ('-need_export', 'email')
    list_filter = (SubscriberGroupFilter, StatusFilter, )
    search_fields = ('email', 'name', 'last_name', 'company')
    list_display = ('email', 'sent', 'opened', 'clicked', 'status', 'is_synced', 'date_created')

    class Media:
        js = (
            'autocomplete/js/select2.min.js',
            'autocomplete/js/select2_cached.js',
            'autocomplete/js/select2_locale_%s.js' % get_language(),
            'autocomplete/js/filter.js',
        )
        css = {
            'all': (
                'autocomplete/css/select2.css',
            )
        }

    def get_suit_form_tabs(self, request, add=False):
        if request.user.is_superuser:
            return (
                ('general', _('General')),
                ('statistics', _('Statistics')),
                ('debug', _('Debugging')),
            )
        else:
            return (
                ('general', _('General')),
                ('statistics', _('Statistics')),
            )

    def get_readonly_fields(self, request, obj=None):
        default = super().get_readonly_fields(request, obj)
        if obj is None or not obj.remote_id:
            # добавление
            return default

        if not request.user.is_superuser:
            default = ('email', 'groups', ) + default
        return default

    def save_model(self, request, obj, form, change):
        """ Автоматически добавляем все группы, если они не заданы """
        super().save_model(request, obj, form, change)
        if not obj.groups.count() and Group.objects.count() <= 1:
            obj.groups.add(*Group.objects.all())

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        default = super().has_delete_permission(request, obj)
        if obj is None:
            return default
        return not obj.remote_id

    def is_synced(self, obj):
        return not obj.need_export
    is_synced.short_description = _('Synchronized')
    is_synced.admin_order_field = 'need_export'
    is_synced.boolean = True
