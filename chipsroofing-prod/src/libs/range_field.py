from django.db import models, connection
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.functional import cached_property


class RangeField(models.IntegerField):
    """
        Поле, аналогичное IntegerField, добавляющее параметры min_value / max_value,
        которые добавляют к полю <input type="number"> атрибуты min / max.

        Пример:
            year = RangeField(_('year'), min_value=1960, max_value=2100)
    """
    def __init__(self, *args, min_value=None, max_value=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.min_value is not None:
            kwargs['min_value'] = self.min_value
        if self.max_value is not None:
            kwargs['max_value'] = self.max_value
        return name, path, args, kwargs

    @cached_property
    def validators(self):
        range_validators = []
        internal_type = self.get_internal_type()
        min_value, max_value = connection.ops.integer_field_range(internal_type)

        min_value = min_value or self.min_value
        if min_value is not None:
            range_validators.append(MinValueValidator(min_value))

        max_value = max_value or self.max_value
        if max_value is not None:
            range_validators.append(MaxValueValidator(max_value))

        return super(models.IntegerField, self).validators + range_validators

    def formfield(self, **kwargs):
        defaults = {
            'min_value': self.min_value,
            'max_value': self.max_value,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
