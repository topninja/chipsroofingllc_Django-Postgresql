from django.db import models
from django.core import exceptions
from django.core.validators import MinValueValidator
from .valute import Valute

DEFAULT_MAX_DIGITS = 18
DEFAULT_DECIMAL_PLACES = 2


class ValuteField(models.DecimalField):
    default_validators = [
        MinValueValidator(0),
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', 0)
        kwargs.setdefault('max_digits', DEFAULT_MAX_DIGITS)
        kwargs.setdefault('decimal_places', DEFAULT_DECIMAL_PLACES)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs['default'] == 0:
            del kwargs['default']
        if kwargs['max_digits'] == DEFAULT_MAX_DIGITS:
            del kwargs['max_digits']
        if kwargs['decimal_places'] == DEFAULT_DECIMAL_PLACES:
            del kwargs['decimal_places']
        return name, path, args, kwargs

    def from_db_value(self, value, *args, **kwargs):
        if value is None:
            return value

        try:
            return Valute(value)
        except (ValueError, TypeError):
            return None

    def get_db_prep_save(self, value, connection):
        value = self.to_python(value)
        if value is None:
            return None if self.null else 0

        return connection.ops.value_to_db_decimal(
            value.as_decimal(),
            self.max_digits,
            self.decimal_places
        )

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None

        if not isinstance(value, Valute):
            value = Valute(value)

        return value.as_decimal()

    def to_python(self, value):
        if value is None:
            return None

        if isinstance(value, Valute):
            return value

        try:
            return Valute(value)
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def run_validators(self, value):
        return super().run_validators(value.as_decimal())
