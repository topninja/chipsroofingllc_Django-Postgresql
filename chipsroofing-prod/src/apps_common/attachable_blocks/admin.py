from django import forms
from django.apps import apps
from django.core import checks
from django.contrib import admin
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.admin import BaseGenericInlineFormSet, GenericInlineModelAdminChecks
from suit.admin import SortableGenericTabularInline, SortableGenericStackedInline
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from libs.autocomplete.widgets import AutocompleteWidget
from .models import AttachableBlock, AttachableReference


def get_block_types():
    """
        Возвращает список content_type_id всех блоков и их названий
    """
    if 'attachable_block_types' not in cache:
        blocks = []
        for model in apps.get_models():
            if issubclass(model, AttachableBlock) and model != AttachableBlock:
                ct = ContentType.objects.get_for_model(model)
                blocks.append((ct.pk, str(model._meta.verbose_name)))

        blocks = tuple(sorted(blocks, key=lambda x: x[1]))
        cache.set('attachable_block_types', blocks, timeout=30 * 60)

    return cache.get('attachable_block_types')


class AttachableBlockAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'label', 'visible'
            ),
        }),
    )
    list_display = ('label', 'visible')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class AttachedBlocksForm(forms.ModelForm):
    block_type = forms.TypedChoiceField(
        coerce=int,
        label=_('Type'),
        choices=get_block_types,
    )

    class Meta:
        fields = '__all__'
        widgets = {
            'block': AutocompleteWidget(
                filters=(('content_type', '__prefix__-block_type', False),),
                expressions="label__icontains",
            ),
        }

    class Media:
        js = (
            'attachable_blocks/admin/js/related.js',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['block_type'] = self.instance.block.content_type_id
        else:
            blocks = list(self.fields['block_type'].choices)
            if blocks:
                self.initial['block_type'] = blocks[0][0]


class AttachedBlocksFormset(BaseGenericInlineFormSet):
    """ Формсет, устанавливающий объектам set_name """
    @property
    def empty_form(self):
        form = super().empty_form
        form.instance.set_name = self.set_name
        return form

    def save_new(self, form, commit=True):
        setattr(form.instance, 'set_name', self.set_name)
        setattr(form.instance, 'block_ct_id', form.cleaned_data.get('block_type'))
        return super().save_new(form, commit)

    def save_existing(self, form, instance, commit=True):
        setattr(form.instance, 'set_name', self.set_name)
        setattr(form.instance, 'block_ct_id', form.cleaned_data.get('block_type'))
        return super().save_existing(form, instance, commit)


class BaseAttachedBlocksMixinChecks(GenericInlineModelAdminChecks):
    def check(self, cls, parent_model, **kwargs):
        errors = super().check(cls, parent_model, **kwargs)
        errors.extend(self._check_set_name(cls))
        return errors

    def _check_set_name(self, cls):
        if not cls.set_name:
            return [
                checks.Error(
                    'set_name can\'t be empty',
                    obj=cls
                )
            ]
        else:
            return []


class BaseAttachedBlocksMixin(ModelAdminInlineMixin):
    """ Базовый класс inline-моделей """
    form = AttachedBlocksForm
    formset = AttachedBlocksFormset
    model = AttachableReference
    fields = ['block_type', 'block', 'ajax']
    superuser_fields = ('ajax', )
    readonly_fields = ('set_name',)
    extra = 0
    set_name = 'default'
    verbose_name = _('block')
    verbose_name_plural = _('Page blocks')

    def get_formset(self, request, obj=None, **kwargs):
        FormSet = super().get_formset(request, obj, **kwargs)
        FormSet.set_name = self.set_name
        return FormSet

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(set_name=self.set_name)


class AttachedBlocksTabularInline(BaseAttachedBlocksMixin, SortableGenericTabularInline):
    """ Родительская модель для tabular инлайнов """
    checks_class = BaseAttachedBlocksMixinChecks
    sortable = 'sort_order'


class AttachedBlocksStackedInline(BaseAttachedBlocksMixin, SortableGenericStackedInline):
    """ Родительская модель для stacked инлайнов """
    checks_class = BaseAttachedBlocksMixinChecks
    sortable = 'sort_order'
