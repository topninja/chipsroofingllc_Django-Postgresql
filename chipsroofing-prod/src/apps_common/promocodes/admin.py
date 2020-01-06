from django import forms
from django.db.models import Q
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from project.admin.filters import HierarchyFilter
from .models import PromoSettings, PromoCode
from .strategies import STRATEGIES


@admin.register(PromoSettings)
class PromoSettingsAdmin(ModelAdminMixin, SingletonModelAdmin):
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


class PromoCodeTypeFilter(HierarchyFilter):
    title = _('Type')
    parameter_name = 'type'
    default_value = 'self-created'

    TYPES = (
        ('all', _('All')),
        ('self-created', _('Self-created')),
        ('auto-generated', _('Auto-generated')),
    )

    def lookups(self, request, model_admin):
        result = []
        for key, name in self.TYPES:
            qs = self.queryset(request, model_admin.model._default_manager, key)
            result.append((key, '%s (%d)' % (name, qs.count())))

        return result

    def get_branch_choices(self, value):
        return [
            (value, dict(self.TYPES).get(value))
        ]

    def queryset(self, request, queryset, value=None):
        value = value or self.value()
        if value == 'self-created':
            queryset = queryset.filter(self_created=True)
        elif value == 'auto-generated':
            queryset = queryset.filter(self_created=False)
        return queryset


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = '__all__'
        widgets = {
            'code': forms.TextInput({
                'class': 'input-large'
            }),
            'parameter': forms.TextInput({
                'class': 'input-small'
            }),
        }

    class Media:
        css = {
            'all': (
                'promocodes/admin/css/promocode.css',
            )
        }

    def clean(self):
        cleaned_data = super().clean()

        code = cleaned_data.get('code')
        query = Q(code__iexact=code)
        if self.instance and self.instance.pk:
            query &= ~Q(pk=self.instance.pk)

        try:
            self._meta.model.objects.get(query)
        except self._meta.model.DoesNotExist:
            pass
        else:
            self.add_error('code', _("%(model_name)s with this %(field_label)s already exists.") % {
                'model_name': self._meta.model._meta.verbose_name.capitalize(),
                'field_label': 'code',
            })

        strategy_name = cleaned_data.get('strategy_name', '')
        if strategy_name:
            cleaned_data = STRATEGIES[strategy_name].validate_form(self, cleaned_data)

        return cleaned_data


@admin.register(PromoCode)
class PromoCodeAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title', 'code',
            ),
        }),
        (_('Action'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'strategy_name', 'parameter',
            ),
        }),
        (_('Limits'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'redemption_limit', 'start_date', 'end_date',
            ),
        }),
    )
    form = PromoCodeForm
    list_display = (
        '__str__', 'code', 'strategy_format', 'times_used', 'redemption_limit_format', 'start_date', 'end_date'
    )
    list_filter = (PromoCodeTypeFilter, )
    list_display_links = ('__str__', 'code')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def strategy_format(self, obj):
        strategy = STRATEGIES.get(obj.strategy_name)
        return strategy.full_description(obj) if strategy else None
    strategy_format.admin_order_field = 'strategy'
    strategy_format.short_description = _('Strategy')

    def times_used(self, obj):
        return obj.times_used
    times_used.short_description = _('Times Used')

    def redemption_limit_format(self, obj):
        if obj.redemption_limit:
            return obj.redemption_limit
        else:
            return _('Unlimited')
    redemption_limit_format.admin_order_field = 'redemption_limit'
    redemption_limit_format.short_description = _('Redemption limit')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.self_created = True
        super().save_model(request, obj, form, change)
