from django.db import models
from django.core import exceptions
from django.contrib.gis.geos import HAS_GEOS
from django.utils.translation import ugettext_lazy as _
from libs.coords import Coords
from .forms import GoogleCoordsFormsField


class GoogleCoordsField(models.Field):
    def __init__(self, *args, **kwargs):
        self.zoom = kwargs.pop('zoom', None)
        kwargs['max_length'] = 32
        kwargs.setdefault('help_text', _('Double click on the map places marker'))
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, *args, **kwargs):
        if not value:
            return None

        try:
            return Coords(*value.split(','))
        except (ValueError, TypeError):
            return None

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if not value:
            return ''

        if not isinstance(value, Coords):
            value = Coords(*value.split(','))

        return str(value)

    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, Coords):
            return value

        try:
            return Coords(*value.split(','))
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def get_db_prep_lookup(self, lookup_type, value, *args, **kwargs):
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': GoogleCoordsFormsField,
            'zoom': self.zoom,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


if HAS_GEOS:
    from django.contrib.gis.db.models import GeometryField, PointField

    class GoogleGISCoordsField(PointField):
        def __init__(self, *args, **kwargs):
            self.zoom = kwargs.pop('zoom', None)
            kwargs.setdefault('help_text', _('Double click on the map places marker'))
            super().__init__(*args, **kwargs)

        def from_db_value(self, value, *args, **kwargs):
            value = super().from_db_value(value, *args, **kwargs)
            if not value:
                return None

            try:
                return Coords(str(value.y), str(value.x))
            except (ValueError, TypeError):
                return None

        def to_python(self, value):
            if not value:
                return None

            if isinstance(value, Coords):
                return value

            try:
                return Coords(*value.split(','))
            except (TypeError, ValueError) as e:
                raise exceptions.ValidationError(e)

        def get_prep_value(self, value):
            if isinstance(value, Coords):
                value = value.get_point(srid=self.srid)

            value = super().get_prep_value(value)
            return value

        def contribute_to_class(self, cls, name, **kwargs):
            super(GeometryField, self).contribute_to_class(cls, name, **kwargs)

        def formfield(self, **kwargs):
            defaults = {
                'form_class': GoogleCoordsFormsField,
                'zoom': self.zoom,
            }
            defaults.update(kwargs)
            return super(GeometryField, self).formfield(**defaults)
