from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.admin.views.main import ChangeList
from mptt.models import MPTTModel
from mptt.admin import MPTTModelAdmin
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey
from mptt.querysets import TreeQuerySet
from mptt.exceptions import InvalidMove
from suit.admin import SortableModelAdmin

__all__ = ['MPTTModel', 'TreeForeignKey', 'MPTTQuerySet', 'InvalidMove',
           'MPTTQuerySetManager', 'SortableMPTTModelAdmin']


# ========================
#       Fix Queryset
# ========================

class MPTTQuerySet(TreeQuerySet):
    def only(self, *fields):
        mptt_meta = self.model._mptt_meta
        mptt_fields = tuple(
            getattr(mptt_meta, key)
            for key in ('left_attr', 'right_attr', 'tree_id_attr', 'level_attr')
        )
        final_fields = set(mptt_fields + fields + tuple(mptt_meta.order_insertion_by))
        return super().only(*final_fields)


class MPTTQuerySetManager(TreeManager):
    _queryset_class = MPTTQuerySet

    def get_leafnodes(self):
        return self._mptt_filter(
            left=(models.F(self.model._mptt_meta.right_attr) - 1)
        )


# ========================
#       Fix ADMIN
# ========================

class SortableMPTTModelAdmin(MPTTModelAdmin, SortableModelAdmin):
    """
        Класс для сортируемого MPTT-дерева.
        Способ, описанный в доках Suit (MPTTModelAdmin, SortableModelAdmin) - косячный.

        https://github.com/darklow/django-suit/issues/381
    """
    def __init__(self, *args, **kwargs):
        super(SortableMPTTModelAdmin, self).__init__(*args, **kwargs)
        mptt_opts = self.model._mptt_meta
        # NOTE: use mptt default ordering
        self.ordering = (mptt_opts.tree_id_attr, mptt_opts.left_attr)
        if self.list_display and self.sortable not in self.list_display:
            self.list_display = list(self.list_display) + [self.sortable]

        self.list_editable = self.list_editable or []
        if self.sortable not in self.list_editable:
            self.list_editable = list(self.list_editable) + [self.sortable]

        self.exclude = self.exclude or []
        if self.sortable not in self.exclude:
            self.exclude = list(self.exclude) + [self.sortable]

    # NOTE: return default admin ChangeList
    def get_changelist(self, request, **kwargs):
        return ChangeList

    def is_bulk_edit(self, request):
        changelist_url = 'admin:%(app_label)s_%(model_name)s_changelist' % {
            'app_label': self.model._meta.app_label,
            'model_name': self.model._meta.model_name,
        }
        return (request.path == reverse(changelist_url) and
                request.method == 'POST' and '_save' in request.POST)

    def save_model(self, request, obj, form, change):
        super(SortableMPTTModelAdmin, self).save_model(request, obj, form, change)
        if not self.is_bulk_edit(request):
            self.model.objects.rebuild()

    def changelist_view(self, request, extra_context=None):
        response = super(SortableMPTTModelAdmin, self).changelist_view(request, extra_context)
        if self.is_bulk_edit(request):
            self.model.objects.rebuild()
        return response
