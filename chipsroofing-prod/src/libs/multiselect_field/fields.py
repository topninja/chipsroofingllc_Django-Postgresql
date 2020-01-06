from collections import Iterable
from django.db import models
from django.core import exceptions, checks
from .forms import MultiSelectFormField


class MultiSelectField(models.Field):
    def __init__(self, *args, coerce=int, splitter=',', **kwargs):
        kwargs.setdefault('max_length', 255)
        self.coerce = coerce
        self.splitter = splitter
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_choices_required())
        errors.extend(self._check_choices_coerce())
        return errors

    def _check_choices_required(self, **kwargs):
        if self._choices is None:
            return [
                checks.Error(
                    "'choices' required",
                    hint=None,
                    obj=self,
                )
            ]
        else:
            return []

    def _check_choices_coerce(self, **kwargs):
        for choice in self.choices:
            try:
                self.coerce(choice[0])
            except (TypeError, ValueError):
                return [
                    checks.Error(
                        "Invalid choice: '%s'" % choice[0],
                        hint=None,
                        obj=self,
                    )
                ]

        return []

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.max_length == 64:
            del kwargs['max_length']
        if self.coerce is not int:
            kwargs['coerce'] = self.coerce
        if self.splitter != ',':
            kwargs['splitter'] = self.splitter
        return name, path, args, kwargs

    def _get_coerced_value(self, value):
        """ Получение множества значений приведенных к типу coerce """
        return set(self.coerce(choice) for choice in value if choice not in self.empty_values)

    def from_db_value(self, value, *args, **kwargs):
        if value is None:
            return None

        return self._get_coerced_value(value.split(self.splitter))

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if not value:
            return ''

        if isinstance(value, Iterable):
            value = self.splitter.join(map(str, value))

        return value

    def to_python(self, value):
        if value is None:
            return None
        elif isinstance(value, (str, bytes)):
            try:
                return self._get_coerced_value(value.split(self.splitter))
            except (TypeError, ValueError):
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        elif isinstance(value, Iterable):
            return self._get_coerced_value(value)
        else:
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def validate(self, value, model_instance):
        if not self.editable:
            # Skip validation for non-editable fields.
            return

        if self._choices and value not in self.empty_values:
            if not isinstance(value, set):
                raise exceptions.ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')

            choices = set(self.coerce(item[0]) for item in self.choices)
            for choice in value:
                if choice not in choices:
                    raise exceptions.ValidationError(
                        self.error_messages['invalid_choice'],
                        code='invalid_choice',
                        params={'value': choice},
                    )

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'], code='null')

        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(self.error_messages['blank'], code='blank')

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        defaults = {
            'choices_form_class': MultiSelectFormField,
            'choices': self.get_choices(include_blank=False),
            'coerce': self.coerce,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
