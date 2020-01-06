import os
import io
import csv
from itertools import islice
from functools import update_wrapper
from django import forms
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.db import transaction
from django.shortcuts import redirect
from django.contrib.admin import helpers
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import truncatechars
from django.contrib.messages import add_message, SUCCESS
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _, ungettext_lazy, get_language
from solo.admin import SingletonModelAdmin
from suit.admin import SortableModelAdmin
from libs.download import AttachmentResponse
from libs.upload import upload_chunked_file, TemporaryFileNotFoundError, NotLastChunk
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from .models import SeoConfig, SeoData, Redirect, Counter, Robots

SEO_TAB_NAME = 'seo'
SEO_FORM_PREFIX = 'seo'


@admin.register(SeoConfig)
class SeoConfigAdmin(ModelAdminMixin, SingletonModelAdmin):
    pass


class CounterForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = SEO_FORM_PREFIX


@admin.register(Counter)
class CounterAdmin(ModelAdminMixin, SortableModelAdmin):
    form = CounterForm
    sortable = 'sort_order'
    list_display = ('__str__', 'position')


class SeoDataAdmin(ModelAdminInlineMixin, admin.ModelAdmin):
    model = SeoData
    fieldsets = (
        (_('Meta tags'), {
            'fields': (
                'title', 'keywords', 'description', 'canonical', 'noindex',
            ),
        }),
        (_('Opengraph'), {
            'fields': (
                'og_title', 'og_image', 'og_description',
            ),
        }),
    )


class SeoModelAdminMixin(ModelAdminMixin):
    """
        Модель админки, добавляющая к форме блок сео-текстов
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_includes = getattr(self, 'suit_form_includes', ())
        self.suit_form_includes = default_includes + (
            ('seo/admin/seo_hint.html', 'top', SEO_TAB_NAME),
            ('seo/admin/seo_form.html', 'bottom', SEO_TAB_NAME),
        )

    def has_seo_permissions(self, request):
        """ Проверка, есть ли права на редактирование SEO """
        return request.user.has_perm('seo.change_seodata')

    def get_suit_form_tabs(self, request, add=False):
        """ Показываем вкладку SEO, если есть права """
        default = super().get_suit_form_tabs(request, add)
        if self.has_seo_permissions(request):
            default = default + ((SEO_TAB_NAME, _('SEO')), )
        return default

    def get_seo_form(self, request, obj=None, change=False):
        """ Получение формы SeoData, связанной с сущностью """
        content_type = ContentType.objects.get_for_model(self.model)
        seo_model_admin = SeoDataAdmin(SeoData, self.admin_site)
        seo_instance = None
        seo_model_form_initial = {}

        if change:
            try:
                seo_instance = SeoData.objects.get(
                    content_type=content_type,
                    object_id=obj.id,
                )
            except (SeoData.DoesNotExist, SeoData.MultipleObjectsReturned):
                pass

        seo_model_form = seo_model_admin.get_form(request, seo_instance)
        seo_model_form_initial.update(seo_model_admin.get_changeform_initial_data(request))

        if request.method == 'POST':
            return seo_model_form(
                request.POST,
                request.FILES,
                instance=seo_instance,
                initial=seo_model_form_initial,
                prefix=SEO_FORM_PREFIX
            )
        else:
            return seo_model_form(
                instance=seo_instance,
                initial=seo_model_form_initial,
                prefix=SEO_FORM_PREFIX
            )

    def save_seo_form(self, request, obj, change=False):
        """ Сохранение формы SeoData, связанной с сущностью """
        if not self.has_seo_permissions(request):
            return

        seo_model_admin = SeoDataAdmin(SeoData, self.admin_site)
        seo_form = self.get_seo_form(request, obj, change=change)

        if seo_form.is_valid() and seo_form.has_changed():
            is_add = seo_form.instance.pk is None
            content_type = ContentType.objects.get_for_model(self.model)

            seo_instance = seo_model_admin.save_form(request, seo_form, change=not is_add)
            seo_instance.content_type = content_type
            seo_instance.object_id = obj.id
            seo_model_admin.save_model(request, seo_instance, seo_form, change=not is_add)

            if is_add:
                seo_model_admin.log_addition(request, seo_instance)
            else:
                change_message = seo_model_admin.construct_change_message(request, seo_form, None)
                seo_model_admin.log_change(request, seo_instance, change_message)

    def response_add(self, request, obj, *args, **kwargs):
        self.save_seo_form(request, obj, change=False)
        return super().response_add(request, obj, *args, **kwargs)

    def response_change(self, request, obj, *args, **kwargs):
        self.save_seo_form(request, obj, change=True)
        return super().response_change(request, obj, *args, **kwargs)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        seo_model_admin = SeoDataAdmin(SeoData, self.admin_site)
        seo_form = self.get_seo_form(request, obj, change=change)

        context['seoDataForm'] = helpers.AdminForm(
            seo_form,
            list(seo_model_admin.get_fieldsets(request, seo_form.instance)),
            seo_model_admin.get_prepopulated_fields(request, seo_form.instance),
            seo_model_admin.get_readonly_fields(request, seo_form.instance),
            model_admin=seo_model_admin
        )
        return super().render_change_form(request, context, add, change, form_url, obj)

    def delete_model(self, request, obj):
        """ Удаление SeoData при удалении сущности """
        content_type = ContentType.objects.get_for_model(self.model)
        seo_data = SeoData.objects.filter(
            content_type=content_type,
            object_id=obj.id,
        )

        super().delete_model(request, obj)
        seo_data.delete()


@admin.register(Robots)
class DummyRobotsAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (_('Content'), {
            'fields': ('text',)
        }),
    )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.robots_file = os.path.join(settings.PUBLIC_DIR, 'robots.txt')
        default_includes = getattr(self, 'suit_form_includes', ())
        self.suit_form_includes = default_includes + (
            ('seo/admin/robots_include.html', 'bottom'),
        )

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        urls = [
            url(r'^$', wrap(self.change_view), name='%s_%s_add' % info),
        ]
        return urls

    def get_changeform_initial_data(self, request):
        if not os.path.isdir(settings.PUBLIC_DIR):
            os.mkdir(settings.PUBLIC_DIR, 0o755)

        if os.path.isfile(self.robots_file):
            try:
                with open(self.robots_file, 'r') as fp:
                    content = fp.read()
            except (PermissionError, FileNotFoundError):
                raise PermissionDenied
        else:
            content = ''

        return {
            'text': content
        }

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        return self.changeform_view(request, form_url=form_url, extra_context=extra_context)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        try:
            fd = os.open(self.robots_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode=0o774)
            os.write(fd, obj.text.encode())
            os.close(fd)
        except (PermissionError, FileNotFoundError):
            raise PermissionDenied

    def response_post_save_add(self, request, obj):
        info = self.model._meta.app_label, self.model._meta.model_name
        return redirect('admin:%s_%s_add' % info)


@admin.register(Redirect)
class RedirectAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_list_template = 'seo/admin/change_list_redirects.html'
    list_display = ('old_path', 'new_path', 'permanent', 'short_note', 'created', 'last_usage')
    search_fields = ('old_path', 'new_path')

    class Media:
        js = (
            'common/js/plupload/plupload.full.min.js',
            'common/js/plupload/i18n/%s.js' % (get_language(),),
            'common/js/uploader.js',
            'seo/admin/js/upload_csv.js',
        )
        css = {
            'all': (
                'seo/admin/css/upload_csv.css',
            )
        }

    def short_note(self, obj):
        return truncatechars(obj.note, 36)
    short_note.short_description = _('Note')

    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        csv_urls = [
            url(
                r'^upload_csv/$',
                self.admin_site.admin_view(self.upload_csv),
                name='%s_%s_upload_csv' % info
            ),
            url(
                r'^download_csv/$',
                self.admin_site.admin_view(self.download_csv),
                name='%s_%s_download_csv' % info
            ),
        ]
        return csv_urls + urls

    def download_csv(self, request):
        class Echo(object):
            def write(self, value):
                return value

        pseudo_buffer = Echo()
        csv_writer = csv.writer(pseudo_buffer)
        stream = (
            csv_writer.writerow([
                rule['old_path'],
                rule['new_path'],
                int(rule['permanent']),
                rule['note'],
                rule['created'],
            ])
            for rule in Redirect.objects.values()
        )
        return AttachmentResponse(request, stream, filename='redirects.csv')

    def upload_csv(self, request):
        try:
            csvfile = upload_chunked_file(request, 'csv')
        except TemporaryFileNotFoundError as e:
            return JsonResponse({
                'message': str(e),
            }, status=400)
        except NotLastChunk:
            return JsonResponse({})

        added_count = 0
        csv_reader = csv.reader(io.TextIOWrapper(csvfile.file))
        while True:
            data = tuple(
                {
                    'old_path': row[0],
                    'new_path': row[1],
                    'permanent': bool(int(row[2])),
                    'note': row[3],
                    'created': row[4],
                }
                for row in islice(csv_reader, 100)
            )
            if not data:
                break

            with transaction.atomic():
                for record in data:
                    old_path = record.pop('old_path', None)
                    new_path = record.pop('new_path', None)
                    if not old_path or not new_path:
                        continue

                    rule, created = Redirect.objects.update_or_create(
                        old_path=old_path,
                        new_path=new_path,
                        defaults=record,
                    )
                    if created:
                        added_count += 1

        csvfile.close()
        add_message(request, SUCCESS,
            ungettext_lazy(
                'Successfully added %d rule.',
                'Successfully added %d rules.',
                number=added_count
            ) % added_count
        )
        return JsonResponse({
            'redirect': reverse('admin:seo_redirect_changelist'),
        })
