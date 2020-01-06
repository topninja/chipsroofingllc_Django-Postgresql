from django.db import models
from django.db.models import signals
from django.db.models.fields import files


class FieldFileMixin:
    def save(self, name, content, save=True, old_value=None):
        super().save(name, content, save=save)
        if old_value and old_value != self.name:
            self.storage.delete(old_value)
    save.alters_data = True


class FieldFile(FieldFileMixin, files.FieldFile):
    pass


class ImageFieldFile(FieldFileMixin, files.ImageFieldFile):
    pass


class FileFieldMixin:
    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        signals.post_delete.connect(self._post_delete, sender=cls)

    def save_form_data(self, instance, data):
        old_value = self.value_from_object(instance)
        setattr(instance, '_%s' % self.attname, old_value)
        super().save_form_data(instance, data)

    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)
        if file and not file._committed:
            old_value = getattr(model_instance, '_%s' % self.attname, None)
            file.save(file.name, file, save=False, old_value=old_value)
        return file

    def _post_delete(self, instance, **kwargs):
        field_file = self.value_from_object(instance)
        field_file.delete(save=False)


class FileField(FileFieldMixin, models.FileField):
    attr_class = FieldFile


class ImageField(FileFieldMixin, models.ImageField):
    attr_class = ImageFieldFile
