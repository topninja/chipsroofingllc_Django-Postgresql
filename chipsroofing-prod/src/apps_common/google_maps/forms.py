from django import forms
from django.core import exceptions
from libs.coords import Coords
from .widgets import GoogleCoordsAdminWidget


class GoogleCoordsFormsField(forms.CharField):
    widget = GoogleCoordsAdminWidget

    def __init__(self, *args, **kwargs):
        self.zoom = kwargs.pop('zoom', None)
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if self.zoom is not None:
            attrs['data-zoom'] = self.zoom
        return attrs

    def to_python(self, value):
        if value in self.empty_values:
            return None

        try:
            return Coords(*value.split(','))
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)
