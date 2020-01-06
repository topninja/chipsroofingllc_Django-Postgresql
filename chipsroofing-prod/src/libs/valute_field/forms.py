from django import forms
from django.core import exceptions
from .valute import Valute
from .widget import ValuteWidget


class ValuteFormField(forms.DecimalField):
    widget = ValuteWidget

    def to_python(self, value):
        value = super().to_python(value)
        if value is None:
            return None

        try:
            return Valute(value)
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)

    def validate(self, value):
        if isinstance(value, Valute):
            value = value.as_decimal()
        return super().validate(value)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({
            'class': 'input-small',
        })
        return attrs
