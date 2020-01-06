from itertools import groupby
from django import forms
from django.utils.encoding import smart_text


class GroupedModelChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, group_by=None, is_relation=False, **kwargs):
        self.group_by = group_by
        self.is_relation = is_relation
        super().__init__(*args, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)

    choices = property(_get_choices, forms.ModelChoiceField._set_choices)


class GroupedModelChoiceIterator(forms.models.ModelChoiceIterator):
    def __iter__(self):
        if self.field.group_by is None:
            yield from super().__iter__()
            return

        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)

        qs = self.queryset
        if self.field.is_relation:
            if self.field.group_by not in qs.query.order_by:
                qs.query.order_by.insert(0, self.field.group_by)
            qs = qs.select_related(self.field.group_by)

        groups = groupby(
            qs.all(),
            key=lambda row: getattr(row, self.field.group_by)
        )
        for group, choices in groups:
            yield smart_text(group), [self.choice(ch) for ch in choices]
