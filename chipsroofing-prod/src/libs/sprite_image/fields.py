from django.db import models
from django.core import exceptions, checks
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import get_finders
from .forms import SpriteImageFormField
from .widgets import SpriteImageWidget
from .icon import Icon


class SpriteImageDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        value = instance.__dict__[self.field.name]

        key = str(value)
        choices_dict = dict(self.field.choices)
        icon = self.field.attr_class(self.field.sprite_url, key, choices_dict.get(key, ()), self.field.size)
        instance.__dict__[self.field.name] = icon

        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value


class SpriteImageField(models.CharField):
    descriptor_class = SpriteImageDescriptor
    attr_class = Icon

    def __init__(self, *args, sprite='', size=(), background='#FFFFFF', **kwargs):
        kwargs.setdefault('max_length', 100)
        super().__init__(*args, **kwargs)
        self.sprite = sprite
        self.sprite_url = staticfiles_storage.url(self.sprite)
        self.background = background
        self.size = size

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['sprite'] = self.sprite
        kwargs['size'] = self.size
        kwargs['background'] = self.background
        if kwargs['max_length'] == 100:
            del kwargs['max_length']
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_blank(**kwargs))
        errors.extend(self._check_sprite_attribute(**kwargs))
        errors.extend(self._check_size_attribute(**kwargs))
        errors.extend(self._check_background_attribute(**kwargs))
        return errors

    def _check_blank(self, **kwargs):
        if getattr(self, 'blank', False):
            return [
                checks.Error(
                    'SpriteImageField cannot have blank=True',
                    obj=self,
                )
            ]
        return []

    def _check_sprite_attribute(self, **kwargs):
        if not self.sprite:
            return [
                checks.Error(
                    'sprite file path required',
                    obj=self
                )
            ]
        else:
            for finder in get_finders():
                result = finder.find(self.sprite, all=True)
                if result:
                    return []
            else:
                return [
                    checks.Error(
                        'sprite file not found: %s' % self.sprite,
                        obj=self
                    )
                ]

    def _check_size_attribute(self, **kwargs):
        if not self.size:
            return [
                checks.Error(
                    'size required',
                    obj=self
                )
            ]
        elif not isinstance(self.size, (list, tuple)) or len(self.size) != 2:
            return [
                checks.Error(
                    'size should be a two-element list or tuple',
                    obj=self
                )
            ]
        else:
            return []

    def _check_background_attribute(self, **kwargs):
        if self.background is None:
            return []

        if not isinstance(self.background, str):
            return [
                checks.Error(
                    'background should be a string, like "#FFDA00"',
                    obj=self
                )
            ]

        return []

    def contribute_to_class(self, cls, *args, **kwargs):
        super().contribute_to_class(cls, *args, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))

    def validate(self, value, model_instance):
        """
        Validates value and throws ValidationError. Subclasses should override
        this to provide validation logic.
        """
        if not self.editable:
            # Skip validation for non-editable fields.
            return

        if self._choices and value not in self.empty_values:
            for option_key, option_value in self.choices:
                if value == option_key:
                    return
            raise exceptions.ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': value},
            )

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'], code='null')

        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(self.error_messages['blank'], code='blank')

    def formfield(self, **kwargs):
        defaults = {
            'choices_form_class': SpriteImageFormField,
            'widget': SpriteImageWidget(
                sprite=self.sprite_url,
                size=self.size,
                background=self.background,
            ),
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
