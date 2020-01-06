from django import forms
from django.core import exceptions
from .color import Color
from .widgets import ColorWidget, ColorOpacityWidget


class ColorFormField(forms.CharField):
    widget = ColorWidget

    def to_python(self, value):
        value = super().to_python(value)

        if not value:
            return None

        try:
            return Color(value)
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)


class ColorOpacityFormField(ColorFormField):
    widget = ColorOpacityWidget
