from django.db import models
from django.core import exceptions, checks
from .color import Color


class ColorField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 12)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.max_length == 12:
            del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, *args, **kwargs):
        if not value:
            return None

        try:
            return Color(value)
        except (ValueError, TypeError):
            return None

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if not value:
            return ''

        if not isinstance(value, Color):
            value = Color(value)

        return value.db_value

    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, Color):
            return value

        try:
            return Color(value)
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)


class ColorOpacityField(ColorField):
    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_choices_allowed(**kwargs))
        return errors

    def _check_choices_allowed(self, **kwargs):
        if self.choices:
            return [
                checks.Error(
                    'choices are not allowed',
                    obj=self
                )
            ]
        else:
            return []
