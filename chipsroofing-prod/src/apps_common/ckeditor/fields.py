from django.db import models
from django.core import checks
from django.db.models import signals
from django.utils.encoding import smart_text
from .forms import CKEditorFormField, CKEditorUploadFormField
from .models import PagePhoto, PageFile, SimplePhoto
from . import conf


class CKEditorField(models.Field):
    """ Текстовое поле с WISYWIG редактором """
    def __init__(self, *args, editor_options=None, height=300, **kwargs):
        editor_options = editor_options or conf.CKEDITOR_CONFIG_DEFAULT
        self.editor_options = editor_options.copy()
        self.editor_options['height'] = int(height)
        if 'contentsCss' not in self.editor_options:
            self.editor_options['contentsCss'] = conf.CKEDITOR_DEFAULT_CSS
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_options(**kwargs))
        return errors

    def _check_options(self, **kwargs):
        if not self.editor_options:
            return [
                checks.Error(
                    'options required',
                    obj=self
                )
            ]
        elif not isinstance(self.editor_options, dict):
            return [
                checks.Error(
                    'options must be a dict',
                    obj=self
                )
            ]
        else:
            return []

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if isinstance(value, str) or value is None:
            return value
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': CKEditorFormField,
            'editor_options': self.editor_options,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class CKEditorUploadField(models.Field):
    """ Текстовое поле с WISYWIG редактором и возможностью загрузки картинок """
    _page_photos = ()
    _page_files = ()
    _simple_photos = ()

    def __init__(self, *args, editor_options=None, height=420, upload_pagephoto_url='',
            upload_pagefile_url='', upload_simplephoto_url='', **kwargs):
        editor_options = editor_options or conf.CKEDITOR_UPLOAD_CONFIG_DEFAULT
        self.editor_options = editor_options.copy()
        self.editor_options['height'] = int(height)
        if 'contentsCss' not in self.editor_options:
            self.editor_options['contentsCss'] = conf.CKEDITOR_DEFAULT_CSS
        self.upload_pagephoto_url = upload_pagephoto_url or '/dladmin/ckeditor/upload_pagephoto/'
        self.upload_pagefile_url = upload_pagefile_url or '/dladmin/ckeditor/upload_pagefile/'
        self.upload_simplephoto_url = upload_simplephoto_url or '/dladmin/ckeditor/upload_simplephoto/'
        
        wide_width = max(
            PagePhoto.photo.variations['wide']['size'][0],
            PagePhoto.photo.variations['wide']['max_width']
        )
        wide_height = max(
            PagePhoto.photo.variations['wide']['size'][1],
            PagePhoto.photo.variations['wide']['max_height'],
            round(PagePhoto.photo.min_dimensions[1] * (wide_width / PagePhoto.photo.min_dimensions[0]))
        )
        kwargs.setdefault('help_text', 'Image sizes: from <b>{}x{}</b> to <b>{}x{}</b>'.format(
            PagePhoto.photo.min_dimensions[0],
            PagePhoto.photo.min_dimensions[1],
            wide_width, wide_height,
        ))
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_options(**kwargs))
        return errors

    def _check_options(self, **kwargs):
        if not self.editor_options:
            return [
                checks.Error(
                    'options required',
                    obj=self
                )
            ]
        elif not isinstance(self.editor_options, dict):
            return [
                checks.Error(
                    'options must be a dict',
                    obj=self
                )
            ]
        else:
            return []

    def save_form_data(self, instance, data):
        self._page_photos = ()
        self._page_files = ()
        self._simple_photos = ()
        if isinstance(data, (list, tuple)):
            if len(data) == 4:
                self._page_photos = data[1].split(',') if data[1] else ()
                self._page_files = data[2].split(',') if data[2] else ()
                self._simple_photos = data[3].split(',') if data[3] else ()

            super().save_form_data(instance, data[0])
        else:
            super().save_form_data(instance, data)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if isinstance(value, str) or value is None:
            return value
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': CKEditorUploadFormField,
            'editor_options': self.editor_options,
            'upload_pagephoto_url': self.upload_pagephoto_url,
            'upload_pagefile_url': self.upload_pagefile_url,
            'upload_simplephoto_url': self.upload_simplephoto_url,
            'model': self.model,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def _post_save(self, instance, **kwargs):
        for photo_id in self._page_photos:
            try:
                photo = PagePhoto.objects.get(id=photo_id)
            except (PagePhoto.DoesNotExist, PagePhoto.MultipleObjectsReturned):
                continue
            else:
                photo.instance_id = instance.id
                photo.save()

        for file_id in self._page_files:
            try:
                file = PageFile.objects.get(id=file_id)
            except (PageFile.DoesNotExist, PageFile.MultipleObjectsReturned):
                continue
            else:
                file.instance_id = instance.id
                file.save()

        for photo_id in self._simple_photos:
            try:
                photo = SimplePhoto.objects.get(id=photo_id)
            except (SimplePhoto.DoesNotExist, SimplePhoto.MultipleObjectsReturned):
                continue
            else:
                photo.instance_id = instance.id
                photo.save()

    def _post_delete(self, instance, **kwargs):
        pagephotos = PagePhoto.objects.filter(
            app_name=instance._meta.app_label,
            model_name=instance._meta.model_name,
            instance_id=instance.id)
        pagephotos.delete()

        pagefiles = PageFile.objects.filter(
            app_name=instance._meta.app_label,
            model_name=instance._meta.model_name,
            instance_id=instance.id)
        pagefiles.delete()

        simplephotos = SimplePhoto.objects.filter(
            app_name=instance._meta.app_label,
            model_name=instance._meta.model_name,
            instance_id=instance.id)
        simplephotos.delete()

    def contribute_to_class(self, cls, name, virtual_only=False):
        super().contribute_to_class(cls, name, virtual_only)
        signals.post_save.connect(self._post_save, sender=cls)
        signals.pre_delete.connect(self._post_delete, sender=cls)
