from django.core import checks
from django.conf import settings
from libs.variation_field.fields import VariationImageField
from libs.variation_field.utils import is_size, format_aspects, check_variations, format_variations
from .formfields import StdImageFormField

DEFAULT_SOURCE_QUALITY = getattr(settings, 'STDIMAGE_SOURCE_QUALITY', 95)
DEFAULT_VARIATION_QUALITY = getattr(settings, 'STDIMAGE_VARIATION_QUALITY', 86)
MAX_SIZE_DEFAULT = getattr(settings,  'STDIMAGE_MAX_SIZE', 12*1024*1024)
MIN_DIMENSIONS_DEFAULT = getattr(settings,  'STDIMAGE_MIN_DIMENSIONS', (0, 0))
MAX_DIMENSIONS_DEFAULT = getattr(settings,  'STDIMAGE_MAX_DIMENSIONS', (6000, 6000))
MAX_SOURCE_DIMENSIONS_DEFAULT = getattr(settings,  'STDIMAGE_MAX_SOURCE_DIMENSIONS', (4096, 3072))


class StdImageField(VariationImageField):

    def __init__(self, verbose_name=None, name=None, variations=None, **kwargs):
        self.admin_variation = kwargs.pop('admin_variation', None)
        self.source_quality = kwargs.pop('source_quality', None)
        self.min_dimensions = kwargs.pop('min_dimensions', MIN_DIMENSIONS_DEFAULT)
        self.max_dimensions = kwargs.pop('max_dimensions', MAX_DIMENSIONS_DEFAULT)
        self.max_source_dimensions = kwargs.pop('max_source_dimensions', MAX_SOURCE_DIMENSIONS_DEFAULT)
        self.max_size = kwargs.pop('max_size', MAX_SIZE_DEFAULT)

        self.crop_area = kwargs.pop('crop_area', False)

        # Форматируем вариации
        self._variations = variations
        self.variations = format_variations(variations)

        # Аспекты кропа. По умолчанию будет использоваться первый.
        # Остальные можно использовать с помощью JS
        self._aspects = kwargs.pop('aspects', ())
        self.aspects = format_aspects(self._aspects, self._variations)

        super().__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_min_dimensions_attribute(**kwargs))
        errors.extend(self._check_max_dimensions_attribute(**kwargs))
        errors.extend(self._check_max_source_dimensions_attribute(**kwargs))
        errors.extend(self._check_variations_attribute(**kwargs))
        errors.extend(self._check_admin_variation_attribute(**kwargs))
        errors.extend(self._check_aspects_attribute(**kwargs))
        return errors

    def _check_min_dimensions_attribute(self, **kwargs):
        if not is_size(self.min_dimensions):
            return [
                checks.Error(
                    'min_dimensions should be a tuple of 2 non-negative numbers',
                    obj=self
                )
            ]
        else:
            return []

    def _check_max_dimensions_attribute(self, **kwargs):
        if not is_size(self.max_dimensions):
            return [
                checks.Error(
                    'max_dimensions should be a tuple of 2 non-negative numbers',
                    obj=self
                )
            ]
        else:
            return []

    def _check_max_source_dimensions_attribute(self, **kwargs):
        if not is_size(self.max_source_dimensions):
            return [
                checks.Error(
                    'max_source_dimensions should be a tuple of 2 non-negative numbers',
                    obj=self
                )
            ]
        else:
            return []

    def _check_variations_attribute(self, **kwargs):
        if not self._variations:
            return [
                checks.Error(
                    'variations is required',
                    obj=self
                )
            ]
        elif not isinstance(self._variations, dict):
            return [
                checks.Error(
                    'variations should be a dict',
                    obj=self
                )
            ]

        errors = []
        errors.extend(check_variations(self._variations, self))
        return errors

    def _check_admin_variation_attribute(self, **kwargs):
        if not self.admin_variation:
            return [
                checks.Error(
                    'admin_variation is required',
                    obj=self
                )
            ]
        elif self.admin_variation not in self._variations:
            return [
                checks.Error(
                    'admin_variation "%s" not found in variations' % self.admin_variation,
                    obj=self
                )
            ]
        else:
            return []

    def _check_aspects_attribute(self, **kwargs):
        if self._aspects:
            return []

        errors = []
        aspects = self._aspects if isinstance(self._aspects, tuple) else (self._aspects,)
        for aspect in aspects:
            try:
                float(aspect)
            except (TypeError, ValueError):
                if not isinstance(aspect, str):
                    errors.append(
                        checks.Error(
                            'aspect can be only float or str instance',
                            obj=self
                        )
                    )
                elif aspect not in self._variations:
                    errors.append(
                        checks.Error(
                            'aspect variation not found: %r' % aspect,
                            obj=self
                        )
                    )
                elif not all(d > 0 for d in self._variations[aspect]['size']):
                    errors.append(
                        checks.Error(
                            'aspect should point to full-filled size: %r' % aspect,
                            obj=self
                        )
                    )
        return errors

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['aspects'] = self._aspects
        kwargs['variations'] = self._variations
        if self.min_dimensions != MIN_DIMENSIONS_DEFAULT:
            kwargs['min_dimensions'] = self.min_dimensions
        if self.max_dimensions != MAX_DIMENSIONS_DEFAULT:
            kwargs['max_dimensions'] = self.max_dimensions
        if self.max_source_dimensions != MAX_SOURCE_DIMENSIONS_DEFAULT:
            kwargs['max_source_dimensions'] = self.max_source_dimensions
        if self.max_size != MAX_SIZE_DEFAULT:
            kwargs['max_size'] = self.max_size
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {
            'form_class': StdImageFormField,
            'variations': self.variations,
            'admin_variation': self.admin_variation,
            'crop_area': self.crop_area,
            'min_dimensions': self.min_dimensions,
            'max_dimensions': self.max_dimensions,
            'max_size': self.max_size,
            'aspects': self.aspects,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def get_variations(self, instance):
        """ Возвращает настройки вариаций """
        return self.variations

    def get_source_quality(self, instance):
        """ Возвращает качество исходника, если он сохраняется через PIL """
        return self.source_quality or DEFAULT_SOURCE_QUALITY

    def get_variation_quality(self, instance, variation):
        """ Возвращает качество картинок вариаций по умолчанию """
        return variation.get('quality') or DEFAULT_VARIATION_QUALITY

    def get_max_source_dimensions(self, instance):
        """ Возвращает максимальные размеры исходника картинки """
        return self.max_source_dimensions

    def get_min_dimensions(self, instance):
        """ Возвращает минимальные размеры картинки для загрузки """
        return self.min_dimensions

    def get_max_dimensions(self, instance):
        """ Возвращает максимальные размеры картинки для загрузки """
        return self.max_dimensions

    def get_max_size(self, instance):
        """ Возвращает максимальный вес картинки для загрузки """
        return self.max_size

    def build_source_name(self, instance, image_format):
        """ Построение имени файла исходника """
        ext = image_format.lower()
        if ext == 'jpeg':
            ext = 'jpg'
        return '%s_%s.%s' % (self.name, instance.pk, ext)
