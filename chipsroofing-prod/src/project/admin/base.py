from django import forms
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.admin.utils import quote
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableModelAdmin
from suit.widgets import SuitDateWidget
from google_maps.fields import GoogleCoordsField
from google_maps.widgets import GoogleCoordsAdminWidget
from libs.file_field.fields import FileField, ImageField
from libs.file_field.widgets import FileWidget
from libs.color_field.fields import ColorField, ColorOpacityField
from libs.color_field.forms import ColorFormField, ColorOpacityFormField
from libs.stdimage.fields import StdImageField
from libs.stdimage.widgets import StdImageAdminWidget
from libs.valute_field.fields import ValuteField
from libs.valute_field.forms import ValuteFormField
from libs.videolink_field.fields import VideoLinkField
from .widgets import URLWidget, SplitDateTimeWidget, AutosizedTextarea


class BaseModelAdminMixin:
    formfield_overrides = {
        models.CharField: {
            'widget': forms.TextInput(attrs={
                'class': 'full-width',
            })
        },
        models.EmailField: {
            'widget': forms.EmailInput(attrs={
                'class': 'input-xlarge',
            })
        },
        models.URLField: {
            'widget': URLWidget(attrs={
                'class': 'full-width',
            })
        },
        models.IntegerField: {
            'widget': forms.NumberInput(attrs={
                'class': 'input-small',
            })
        },
        models.TextField: {
            'widget': AutosizedTextarea(attrs={
                'class': 'full-width',
                'rows': 2,
            })
        },
        models.DateField: {
            'widget': SuitDateWidget,
        },
        models.DateTimeField: {
            'widget': SplitDateTimeWidget,
        },
        models.TimeField: {
            'localize': True,
            'widget': forms.TextInput(attrs={
                'class': 'input-medium',
                'placeholder': 'e.g. "11:00 am"',
            }),
        },
        FileField: {
            'widget': FileWidget,
        },
        ImageField: {
            'widget': FileWidget,
        },
        StdImageField: {
            'widget': StdImageAdminWidget,
        },
        ColorField: {
            'form_class': ColorFormField,
        },
        ColorOpacityField: {
            'form_class': ColorOpacityFormField,
        },
        ValuteField: {
            'form_class': ValuteFormField,
        },
        VideoLinkField: {
            'widget': URLWidget(attrs={
                'class': 'full-width',
            }),
        },
        GoogleCoordsField: {
            'widget': GoogleCoordsAdminWidget,
        },
    }

    # поля, которые отображаются только для суперюзера
    superuser_fields = ()

    # поля, которые может редактировать только суперюзер.
    # Для других, поля будут readonly
    superuser_editable_fields = ()

    def get_readonly_fields(self, request, obj=None):
        """
            Блокировка полей, перечисленных в superuser_editable
        """
        fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            fields = tuple(fields) + tuple(self.superuser_editable_fields)
        return fields

    def get_fields(self, request, obj=None):
        """
            Скрытие полей, перечисленных в superuser_fields
        """
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [field for field in fields if field not in self.superuser_fields]
        return fields

    def get_fieldsets(self, request, obj=None):
        """
            Скрытие полей, перечисленных в superuser_fields
        """
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            for name, opts in fieldsets:
                opts['fields'] = tuple(field for field in opts['fields'] if field not in self.superuser_fields)
        return fieldsets


class ModelAdminInlineMixin(BaseModelAdminMixin):
    pass


class ModelAdminMixin(BaseModelAdminMixin):
    actions_on_top = True
    actions_on_bottom = True

    add_form_template = 'suit/change_form.html'
    change_form_template = 'suit/change_form.html'

    @property
    def media(self):
        return super().media + forms.Media(
            js=(
                'admin/js/customize.js',
            ),
        )

    def suit_cell_attributes(self, obj, column):
        """ Классы для ячеек списка """
        if column == 'view':
            return {
                'class': 'mini-column'
            }
        else:
            return {}

    def get_suit_form_tabs(self, request, add=False):
        """ Получение вкладок для модели админки Suit """
        return getattr(self, 'suit_form_tabs', ())

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not self.has_delete_permission(request) and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        """ Получаем вкладки Suit и передаем их в шаблон """
        suit_tabs = self.get_suit_form_tabs(request, add)
        context['suit_tabs'] = suit_tabs
        return super().render_change_form(request, context, add, change, form_url, obj)

    def view(self, obj):
        """ Ссылка просмотра на сайте для отображения в списке сущностей """
        if hasattr(obj, 'get_absolute_url'):
            admin_url = obj.get_absolute_url()
            if admin_url:
                return ('<a href="%s" target="_blank" title="%s">'
                        '   <span class="icon-eye-open icon-alpha75"></span>'
                        '</a>') % (admin_url, _('View on site'))
        return '<span>-//-</span>'
    view.short_description = '#'
    view.allow_tags = True


class ReversedSortableModelAdmin(SortableModelAdmin):
    """
        Аналог SortableModelAdmin, за тем исключением, что
        новые записи добавляются в начало списка, а не в конец.

        Внимание!! Поле сортировки должно поддерживать отрицательные значения!
    """
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            min_order = obj.__class__.objects.aggregate(
                models.Min(self.sortable))
            try:
                next_order = min_order['%s__min' % self.sortable] - 1
            except TypeError:
                next_order = 0
            setattr(obj, self.sortable, next_order)
        super(SortableModelAdmin, self).save_model(request, obj, form, change)


class RealLinksChangeListMixin:
    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        return reverse(
            'admin:%s_%s_change' % (result._meta.app_label, result._meta.model_name),
            args=(quote(pk),),
            current_app=self.model_admin.admin_site.name
        )


class RealLinksModelAdminMixin:
    """
        Миксина для модели админки,
        которая генерирует ссылки на сущности на основе фактических моделей в списке,
        а не на основе модели админки.

        Полезно в случаях, когда get_queryset() возвращает модели разных классов.
    """
    def get_changelist(self, request, **kwargs):
        default = super().get_changelist(request, **kwargs)
        return type('CustomChangeList', (RealLinksChangeListMixin, default), {})
