from django.db import models
from django.core import checks
from .forms import GroupedModelChoiceField


class GroupedForeignKey(models.ForeignKey):
    """
        Поле, группирующее (<optgroup>) список сущностей
        по значению одного из полей этих сущностей.

        Пример:
            # models.py:
                class Category(models.Model):
                    ...

                class Product(models.Model):
                    category = models.ForeignKey(Category)
                    ...

                class ProductProperty(models.Model):
                    product = GroupedForeignKey(Product, group_by='category')
    """
    def __init__(self, *args, group_by=None, **kwargs):
        self.group_by = group_by
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_group_by())
        return errors

    def _check_group_by(self, **kwargs):
        if not isinstance(self.group_by, str):
            return [
                checks.Error(
                    '"group_by" attribute required',
                    obj=self,
                )
            ]

        field = self.rel.to._meta.get_field(self.group_by)
        if not field:
            return [
                checks.Error(
                    'Not found field "%s" in model %s' % (self.group_by, self.rel.to.__name__),
                    obj=self,
                )
            ]
        return []

    def formfield(self, **kwargs):
        field = self.rel.to._meta.get_field(self.group_by)
        defaults = {
            'form_class': GroupedModelChoiceField,
            'group_by': self.group_by,
            'is_relation': field.is_relation,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
