from django.db import models
from django.db.models import signals
from libs.variation_field.fields import VariationImageField
from .formfields import GalleryFormField


class GalleryImageField(VariationImageField):
    def get_variations(self, instance):
        """ Возвращает настройки вариаций для их передачи в FieldFile """
        if not instance.content_type_id:
            # fix для loaddata
            return {}
        return instance.variations()

    def get_source_quality(self, instance):
        """ Возвращает качество исходника, если он сохраняется через PIL """
        return instance.SOURCE_QUALITY

    def get_variation_quality(self, instance, variation):
        """ Возвращает качество картинок вариаций по умолчанию """
        return variation.get('quality') or instance.DEFAULT_QUALITY

    def get_max_source_dimensions(self, instance):
        """ Возвращает максимальные размеры исходника картинки """
        return instance.MAX_SOURCE_DIMENSIONS

    def get_min_dimensions(self, instance):
        """ Возвращает минимальные размеры картинки для загрузки """
        return instance.MIN_DIMENSIONS

    def get_max_dimensions(self, instance):
        """ Возвращает максимальные размеры картинки для загрузки """
        return instance.MAX_DIMENSIONS

    def get_max_size(self, instance):
        """ Возвращает максимальный вес картинки для загрузки """
        return instance.MAX_SIZE

    def build_source_name(self, instance, image_format):
        """ Построение имени файла исходника """
        ext = image_format.lower()
        if ext == 'jpeg':
            ext = 'jpg'
        return '%04d.%s' % (instance.pk, ext)


class GalleryVideoLinkPreviewField(VariationImageField):

    def validate(self, value, model_instance):
        if value:
            self.validate_type(value, model_instance)

        super(VariationImageField, self).validate(value, model_instance)

    def get_variations(self, instance):
        """ Возвращает настройки вариаций для их передачи в FieldFile """
        if not instance.content_type_id:
            # fix для loaddata
            return {}
        return instance.variations()

    def get_source_quality(self, instance):
        """ Возвращает качество исходника, если он сохраняется через PIL """
        return instance.SOURCE_QUALITY

    def get_variation_quality(self, instance, variation):
        """ Возвращает качество картинок вариаций по умолчанию """
        return variation.get('quality') or instance.DEFAULT_QUALITY

    def get_max_source_dimensions(self, instance):
        """ Возвращает максимальные размеры исходника картинки """
        return instance.MAX_SOURCE_DIMENSIONS

    def build_source_name(self, instance, image_format):
        """ Построение имени файла исходника """
        ext = image_format.lower()
        if ext == 'jpeg':
            ext = 'jpg'
        return '%04d.%s' % (instance.pk, ext)


class GalleryField(models.OneToOneField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('on_delete', models.SET_NULL)
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        super().contribute_to_class(cls, name, virtual_only)
        signals.pre_delete.connect(self.pre_delete, sender=cls)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': GalleryFormField,
            'related_model': self.rel.to,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def pre_delete(self, instance=None, **kwargs):
        """ Удаление галереи при удалении сущности """
        gallery = getattr(instance, self.name)
        if gallery:
            gallery.delete()
