from django.db import models
from django.core import checks, exceptions
from .videolink import VideoLink
from .providers import PROVIDERS


class VideoLinkField(models.Field):
    def __init__(self, *args, providers=set(), **kwargs):
        kwargs['max_length'] = 64
        self._providers = set(providers)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        kwargs['providers'] = self._providers
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_providers(**kwargs))
        return errors

    def _check_providers(self, **kwargs):
        if not self._providers:
            return []

        if not isinstance(self._providers, (set, list, tuple)):
            return [
                checks.Error(
                    'providers must be a set, list or tuple',
                    obj=self
                )
            ]

        errors = []
        for provider in self._providers:
            if provider not in PROVIDERS:
                errors.append(
                    checks.Error(
                        'provider unknown: %s' % provider,
                        obj=self
                    )
                )
        return errors

    def from_db_value(self, value, *args, **kwargs):
        if not value:
            return None

        try:
            return VideoLink(value, self._providers)
        except (ValueError, TypeError):
            return None

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if not value:
            return ''

        if not isinstance(value, VideoLink):
            value = VideoLink(value, self._providers)

        return value.db_value

    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, VideoLink):
            return value

        try:
            return VideoLink(value, self._providers)
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
