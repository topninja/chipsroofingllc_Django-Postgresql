import os
from PIL import Image
from concurrent import futures
from django.db import models
from django.db.models import signals
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.files import ImageFieldFile, FieldFile, ImageFileDescriptor
from .croparea import CropArea
from .utils import image_hash, limited_size, process_variation
from . import validation
from . import conf


class VariationField(ImageFile):
    """
        Класс вариации у поля экземпляра модели.
    """
    _file = None

    def __init__(self, name, storage=None, variation_size=(0, 0)):
        super().__init__(None, name)
        self.storage = storage or default_storage
        self.variation_size = variation_size

    @property
    def file(self):
        if not hasattr(self, '_file') or self._file is None:
            self._file = self.storage.open(self.name, 'rb')
        return self._file

    @file.setter
    def file(self, file):
        self._file = file

    @file.deleter
    def file(self):
        del self._file

    def exists(self):
        return self.storage.exists(self.name)

    def open(self, mode='rb'):
        self.file.open(mode)

    def close(self):
        file = getattr(self, '_file', None)
        if file is not None:
            file.close()

    def delete(self):
        if not self:
            return
        # Only close the file if it's already open, which we know by the
        # presence of self._file
        if hasattr(self, '_file'):
            self.close()
            del self.file

        self.storage.delete(self.name)
        self.name = None

    @property
    def dimensions(self):
        if self and (self.exists() or not self.closed):
            return self._get_image_dimensions()
        else:
            return -1, -1

    def clear_dimensions(self):
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache

    @property
    def target_width(self):
        """
            Целевая ширина вариации.
            Для задания атрибута "width" у тэга "img".
        """
        return self.variation_size[0] or self.dimensions[0]

    @property
    def target_height(self):
        """
            Целевая высота вариации.
            Для задания атрибута "height" у тэга "img".
        """
        return self.variation_size[1] or self.dimensions[1]

    @property
    def path(self):
        return self.storage.path(self.name)

    @property
    def url(self):
        return self.storage.url(self.name)

    @property
    def url_nocache(self):
        if self.storage.exists(self.name):
            return self.storage.url(self.name) + '?_=%d' % self.storage.modified_time(self.name).timestamp()
        else:
            return self.storage.url(self.name)

    @property
    def srcset(self):
        width = self.variation_size[0] or self.dimensions[0]
        return '{url} {width}w'.format(url=self.url, width=width)

    @property
    def srcset_nocache(self):
        width = self.dimensions[0]
        return '{url} {width}w'.format(url=self.url_nocache, width=width)

    @property
    def space(self):
        return '%0.2f%%' % (100 * self.height / self.width)

    @property
    def target_space(self):
        return '%0.2f%%' % (100 * self.target_height / self.target_width)

    @property
    def size(self):
        return self.storage.size(self.name)

    @property
    def accessed_time(self):
        return self.storage.accessed_time(self.name)

    @property
    def created_time(self):
        return self.storage.created_time(self.name)

    @property
    def modified_time(self):
        return self.storage.modified_time(self.name)


class VariationImageFieldFile(ImageFieldFile):
    _croparea = ''
    _variations = None

    def __getattr__(self, item):
        if item in self.variations:
            self.create_variations()
            if item in self.__dict__:
                return self.__dict__[item]

        raise AttributeError(
            "'%s' object has no attribute '%s'" % (self.__class__.__name__, item)
        )

    @property
    def dimensions(self):
        """ Реальные размеры изображения """
        if self and (self.exists() or not self.closed):
            return self._get_image_dimensions()
        else:
            return -1, -1

    def clear_dimensions(self):
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache

    def exists(self):
        return self.storage.exists(self.name)

    @property
    def url_nocache(self):
        try:
            mt = self.storage.modified_time(self.name).timestamp()
        except FileNotFoundError:
            mt = 0
        return self.storage.url(self.name) + '?_=%d' % mt

    @property
    def srcset(self):
        width = self.dimensions[0]
        return '{url} {width}w'.format(url=self.url, width=width)

    @property
    def srcset_nocache(self):
        width = self.dimensions[0]
        return '{url} {width}w'.format(url=self.url_nocache, width=width)

    @property
    def space(self):
        return '%0.2f%%' % (100 * self.height / self.width)

    @property
    def croparea(self):
        return self._croparea

    @croparea.setter
    def croparea(self, value):
        """ Форматирование области обрезки картинки """
        if value is None:
            return

        if not value:
            self._croparea = ''
        elif isinstance(value, (list, tuple)):
            self._croparea = CropArea(*value)
        elif isinstance(value, CropArea):
            self._croparea = value
        else:
            self._croparea = CropArea(value)

    @property
    def variations(self):
        field = self.__dict__.get('field')
        if field and self._variations is None:
            variations = field.get_variations(self.instance)
            self._variations = variations
        return self._variations or {}

    @property
    def variation_files(self):
        """
            Возвращает кортеж путей к вариациям файла.
            Существование файлов не гарантировано.
            !!! Пути не учитывают storage !!!
        """
        files_list = []
        for name, variation in self.variations.items():
            path = self.field.build_variation_name(variation, self.instance, self.name)
            files_list.append(path)
        return tuple(files_list)

    def set_crop_field(self, instance, croparea=None):
        self.croparea = croparea
        if self.field.crop_field and hasattr(instance, self.field.crop_field):
            setattr(instance, self.field.crop_field, self.croparea)

    def create_variations(self):
        """
            Создает атрибуты вариаций
        """
        if not self or not self.exists():
            return

        for name, variation in self.variations.items():
            variation_filename = self.field.build_variation_name(variation, self.instance, self.name)
            variation_field = VariationField(
                variation_filename,
                storage=self.storage,
                variation_size=variation['size']
            )
            setattr(self, name, variation_field)

    def recut(self, *args, croparea=''):
        """
            Перенарезка вариаций.

            Пример:
                company.logo.recut('on_list', 'on_news')
                company.logo.recut('on_list', croparea=[0, 12, 310, 177])
        """
        self.field.build_variation_images(self.instance, *args, croparea=croparea)

        if self.field.crop_field:
            self.set_crop_field(self.instance, croparea)
            self.field.update_instance(self.instance, **{
                self.field.crop_field: self.croparea
            })

    def rotate(self, angle=90):
        """
            Поворот вариаций и исходника.

            Потеряется кроп из админки, т.к. выбранная область не сохраняется.
            Углы поворота обратны углам PIL:
                положительные - по часовой стрелке
                отрицательные - против часовой стрелке

            Пример:
                company.logo.rotate(90)
        """
        try:
            self.open()
            source_image = Image.open(self)
            source_format = source_image.format

            source_info = source_image.info
            dest_info = source_info.copy()
            if source_format in (conf.FORMAT_JPEG, conf.FORMAT_PNG):
                dest_info['optimize'] = True

            source_image = source_image.rotate(-angle, expand=True)
            with self.storage.open(self.name, 'wb') as destination:
                source_image.save(destination, source_format, **dest_info)
        finally:
            self.close()

        # Сброс закэшированных размеров
        self.clear_dimensions()

        # Обрабатываем вариации
        self.field.build_variation_images(self.instance)

    def calculateHash(self, hash_size=12):
        """
            Рассчет хэша исходника картинки
        """
        try:
            self.open()
            image = Image.open(self)
            return image_hash(image, hash_size)
        finally:
            self.close()

    def save(self, name, content, save=True):
        newfile_attrname = '_{}_new_file'.format(self.field.name)
        setattr(self.instance, newfile_attrname, True)
        if self.field.crop_field:
            self.set_crop_field(self.instance, '')
        super().save(name, content, save)
    save.alters_data = True

    def delete(self, save=True):
        """ Удаление картинки """
        self.create_variations()
        for name in self.variations.keys():
            variation_field = getattr(self, name, None)
            if variation_field:
                variation_field.delete()
        if self.field.crop_field:
            self.set_crop_field(self.instance, '')
        super().delete(save)
    delete.alters_data = True


class VariationImageFileDescriptor(ImageFileDescriptor):
    def __get__(self, instance=None, owner=None):
        if instance is None:
            return owner._meta.get_field(self.field.name)

        value = super().__get__(instance, owner)

        # Добавляем значение области обрезки
        if self.field.crop_field:
            croparea = getattr(instance, self.field.crop_field)
            try:
                value.croparea = CropArea(croparea)
            except ValueError:
                pass

        return value

    def __set__(self, instance, value):
        if isinstance(value, VariationImageFieldFile):
            if self.field.crop_field:
                value.set_crop_field(instance, value.croparea)

        super().__set__(instance, value)


class VariationImageField(models.ImageField):
    attr_class = VariationImageFieldFile
    descriptor_class = VariationImageFileDescriptor

    default_error_messages = dict(
        models.ImageField.default_error_messages,
        not_image=_("Image invalid or corrupted"),
        not_enough_width=_('Image should not be less than %(limit)spx in width'),
        not_enough_height=_('Image should not be less than %(limit)spx in height'),
        too_much_width=_('Image should not be more than %(limit)spx in width'),
        too_much_height=_('Image should not be more than %(limit)spx in height'),
        too_big=_('Image must be no larger than %(limit)s'),
    )

    def __init__(self, *args, **kwargs):
        self.crop_field = kwargs.pop('crop_field', None)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if isinstance(value, FieldFile) and not value.exists():
            return ''

        return super().get_prep_value(value)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        signals.post_save.connect(self._post_save, sender=cls)
        signals.post_delete.connect(self._post_delete, sender=cls)

    def save_form_data(self, instance, data):
        croparea = None
        if isinstance(data, (list, tuple)):
            data, croparea = data

        # Important: None means "no change", other false value means "clear"
        # This subtle distinction (rather than a more explicit marker) is
        # needed because we need to consume values that are also sane for a
        # regular (non Model-) Form to find in its cleaned_data dictionary.
        if data is not None:
            # This value will be converted to unicode and stored in the
            # database, so leaving False as-is is not acceptable.
            if not data:
                data = ''
                self._post_delete(instance)

            setattr(instance, self.name, data)

            if data and croparea is not None:
                setattr(instance, '_{}_croparea'.format(self.name), croparea)

    def validate(self, value, model_instance):
        if value:
            validation.validate_type(value,
                error_messages=self.error_messages
            )
            validation.validate_dimensions(value,
                min_dimensions=self.get_min_dimensions(model_instance),
                max_dimensions=self.get_max_dimensions(model_instance),
                croparea=value.croparea,
                error_messages=self.error_messages,
            )
            validation.validate_size(value,
                max_size=self.get_max_size(model_instance),
                error_messages=self.error_messages,
            )

        super().validate(value, model_instance)

    def get_variations(self, instance):
        """ Возвращает настройки вариаций """
        raise NotImplementedError()

    def get_source_quality(self, instance):
        """ Возвращает качество исходника, если он сохраняется через PIL """
        raise NotImplementedError()

    def get_variation_quality(self, instance, variation):
        """ Возвращает качество картинок вариаций по умолчанию """
        raise NotImplementedError()

    def get_max_source_dimensions(self, instance):
        """ Возвращает максимальные размеры исходника картинки """
        raise NotImplementedError()

    def get_min_dimensions(self, instance):
        """ Возвращает минимальные размеры картинки для загрузки """
        return 0, 0

    def get_max_dimensions(self, instance):
        """ Возвращает максимальные размеры картинки для загрузки """
        return 6000, 6000

    def get_max_size(self, instance):
        """ Возвращает максимальный вес картинки для загрузки """
        return 20 * 1024 * 1024

    def build_source_name(self, instance, image_format):
        raise NotImplementedError()

    def save_source_file(self, instance, source_image, draft_size=None):
        """ Сохранение исходника """
        field_file = self.value_from_object(instance)
        source_format = source_image.format

        out_name = self.build_source_name(instance, source_format)
        source_path = self.generate_filename(instance, out_name)
        source_path = self.storage.get_available_name(source_path)

        if draft_size is None:
            # Если картинка не менялась - копируем файл
            with self.storage.open(field_file.name) as source:
                self.storage.save(source_path, source)
        else:
            source_info = source_image.info
            dest_info = source_info.copy()

            if source_format in (conf.FORMAT_JPEG, conf.FORMAT_PNG):
                dest_info['optimize'] = True

            quality = self.get_source_quality(instance)
            if quality and source_format == conf.FORMAT_JPEG:
                dest_info['quality'] = quality

            with self.storage.open(source_path, 'wb') as destination:
                source_image.save(destination, source_format, **dest_info)
                source_image.close()

        # Записываем путь к исходнику
        setattr(instance, self.attname, source_path)

        return source_path

    @staticmethod
    def build_variation_name(variation, instance, source_filename):
        """ Возвращает имя файла вариации """
        basename, ext = os.path.splitext(source_filename)
        new_ext = conf.FORMAT_EXT.get(variation['format'])
        if new_ext:
            ext = new_ext
        return ''.join((basename, '.%s' % variation['name'], ext))

    def save_variation_file(self, instance, image, variation, **image_options):
        """
            Сохранение картинки вариации в файл
        """
        field_file = self.value_from_object(instance)
        output = self.build_variation_name(variation, instance, field_file.name)
        with self.storage.open(output, 'wb') as dest:
            image.save(dest, **image_options)

        # Очищаем закэшированные размеры картинки, т.к. они могли измениться
        variation_field = getattr(field_file, variation['name'])
        variation_field.clear_dimensions()

    def build_variation_images(self, instance, *variations, croparea=None):
        """
            Обрезает картинку source_image по заданным координатам
            и создает из результата файлы вариаций.
        """
        field_file = self.value_from_object(instance)
        if not field_file or not field_file.exists():
            return

        field_file.create_variations()

        if conf.VARIATION_THREADS <= 1:
            for name, variation in self.get_variations(instance).items():
                if not variations or name in variations:
                    image, image_options = process_variation(
                        field_file.path,
                        variation,
                        self.get_variation_quality(instance, variation),
                        croparea=croparea
                    )
                    self.save_variation_file(instance, image, variation, **image_options)
        else:
            with futures.ThreadPoolExecutor(max_workers=conf.VARIATION_THREADS) as executor:
                futures_dict = {
                    executor.submit(
                        process_variation,
                        source=field_file.path,
                        variation=variation,
                        quality=self.get_variation_quality(instance, variation),
                        croparea=croparea
                    ): variation
                    for name, variation in self.get_variations(instance).items()
                    if not variations or name in variations
                }

                for future in futures.as_completed(futures_dict):
                    variation = futures_dict[future]
                    image, image_options = future.result()
                    self.save_variation_file(instance, image, variation, **image_options)

    @staticmethod
    def update_instance(instance, **kwargs):
        if not kwargs:
            return
        if not instance.pk:
            raise ValueError('saving image to not saved instance')

        queryset = instance._meta.model.objects.filter(pk=instance.pk)
        queryset.update(**kwargs)

    def _post_save(self, instance, **kwargs):
        """ Обертка над реальным обработчиком """
        # Флаг, что загружен новый файл
        new_file_attrname = '_{}_new_file'.format(self.name)
        new_file_uploaded = getattr(instance, new_file_attrname, False)
        if hasattr(instance, new_file_attrname):
            delattr(instance, new_file_attrname)

        # Координаты обрезки
        croparea_attrname = '_{}_croparea'.format(self.name)
        croparea = getattr(instance, croparea_attrname, None)
        if hasattr(instance, croparea_attrname):
            delattr(instance, croparea_attrname)

        self.post_save(instance, is_uploaded=new_file_uploaded, croparea=croparea, **kwargs)

    def post_save(self, instance, is_uploaded=None, croparea=None, **kwargs):
        """ Обработчик сигнала сохранения экземпляра модели """
        # Если не загрузили новый файл и не обрезали старый исходник - выходим
        if not is_uploaded and not croparea:
            return

        field_file = self.value_from_object(instance)
        if not field_file or not field_file.exists():
            return

        field_file.croparea = croparea

        update_fields = {}

        try:
            field_file.open()
            source_image = Image.open(field_file)
            source_format = source_image.format

            if is_uploaded:
                draft_size = limited_size(
                    source_image.size,
                    self.get_max_source_dimensions(instance)
                )
                if draft_size is not None:
                    old_width = source_image.size[0]
                    draft = source_image.draft(None, draft_size)
                    if draft is None:
                        source_image = source_image.resize(draft_size, Image.HAMMING)
                        source_image.format = source_format

                    # Учитываем изменение размера исходника на области обрезки
                    if field_file.croparea:
                        decr_relation = old_width / source_image.size[0]
                        croparea = tuple(
                            round(coord / decr_relation)
                            for coord in field_file.croparea
                        )
                        field_file.croparea = croparea

                # Сохраняем исходник
                source_path = self.save_source_file(instance, source_image, draft_size=draft_size)
                update_fields[self.attname] = source_path
        finally:
            field_file.close()

            # Удаляем загруженный исходник
            if is_uploaded:
                self.storage.delete(field_file.name)

        # Сохраняем область обрезки в поле, если оно указано
        if croparea and self.crop_field:
            update_fields[self.crop_field] = croparea

        self.update_instance(instance, **update_fields)

        # Обрабатываем вариации
        self.build_variation_images(instance, croparea=field_file.croparea)

    def _post_delete(self, instance=None, **kwargs):
        """ Обработчик сигнала удаления экземпляра модели """
        field_file = self.value_from_object(instance)
        field_file.delete(save=False)

    def recut_all(self, *args):
        """ Перенарезка всех картинок """
        if self.crop_field:
            def get_crop(arg):
                return getattr(arg, self.crop_field)
        else:
            def get_crop(arg):
                return None

        for instance in self.model.objects.all():
            file_field = getattr(instance, self.name)
            if file_field:
                file_field.recut(*args, croparea=get_crop(instance))
