import os
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from libs.stdimage.fields import StdImageField
from libs.storages.media_storage import MediaStorage
from libs.file_field.fields import FileField


def split_by_dirs(instance, filename):
    """ Разбиваем картинки по папкам по 1000 файлов максимум """
    directory = ''
    if instance.pk:
        directory = '%04d' % (instance.pk // 1000)
    return os.path.join(directory, os.path.basename(filename))


class PagePhoto(models.Model):
    """ Модель фото на страницу """
    app_name = models.CharField(_('application'), max_length=30, blank=True)
    model_name = models.CharField(_('model'), max_length=30, blank=True)
    instance_id = models.IntegerField(_('entry id'), db_index=True, default=0)
    photo = StdImageField(_('image'),
        blank=True,
        storage=MediaStorage('page_photos'),
        upload_to=split_by_dirs,
        min_dimensions=(800, 450),
        admin_variation='mobile',
        crop_area=True,
        crop_field='photo_crop',
        aspects='normal',
        variations=dict(
            wide=dict(
                size=(1024, 576),
                quality=88,
            ),
            normal=dict(
                size=(800, 450),
            ),
            mobile=dict(
                size=(480, 270),
            ),
        ))
    photo_crop = models.CharField(_('crop'),
        max_length=32,
        blank=True,
        editable=False,
    )

    class Meta:
        default_permissions = ()
        verbose_name = _('page photo')
        verbose_name_plural = _('page photos')

    def __str__(self):
        return _('Image #%(pk)s for entry %(app)s.%(model)s #%(entry_id)s') % {
            'pk': self.pk,
            'app': self.app_name,
            'model': self.model_name,
            'entry_id': self.instance_id,
        }


class PageFile(models.Model):
    """ Модель файла на страницу """
    MIME_CLASSES = {
        'image/jpeg': 'file-image file-jpg',
        'image/png': 'file-image file-png',
        'image/gif': 'file-image file-gif',
        'text/plain': 'file-text file-txt',
        'text/rtf': 'file-text file-doc',
        'application/msword': 'file-text file-doc',
        'application/xml': 'file-text file-xml',
        'application/pdf': 'file-text file-pdf',
        'application/x-rar': 'file-archive file-rar',
        'application/zip': 'file-archive file-zip',
    }

    app_name = models.CharField(_('application'), max_length=30, blank=True)
    model_name = models.CharField(_('model'), max_length=30, blank=True)
    instance_id = models.IntegerField(_('entry id'), db_index=True, default=0)
    file = FileField(_('file'),
        blank=True,
        storage=MediaStorage('page_files'),
        upload_to=split_by_dirs,
    )

    class Meta:
        default_permissions = ()
        verbose_name = _('page file')
        verbose_name_plural = _('page files')

    def __str__(self):
        return _('File #%(pk)s for entry %(app)s.%(model)s #%(entry_id)s') % {
            'pk': self.pk,
            'app': self.app_name,
            'model': self.model_name,
            'entry_id': self.instance_id,
        }


@receiver(post_delete, sender=PageFile)
def delete_pagefile(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)


class SimplePhoto(models.Model):
    """ Модель фото на страницу """
    app_name = models.CharField(_('application'), max_length=30, blank=True)
    model_name = models.CharField(_('model'), max_length=30, blank=True)
    instance_id = models.IntegerField(_('entry id'), db_index=True, default=0)
    photo = StdImageField(_('image'),
        blank=True,
        storage=MediaStorage('simple_photos'),
        upload_to=split_by_dirs,
        admin_variation='mobile',
        max_source_dimensions=(3072, 3072),
        variations=dict(
            mobile=dict(
                size=(0, 0),
                crop=False,
                max_width=512,
            ),
        )
    )

    class Meta:
        default_permissions = ()
        verbose_name = _('simple photo')
        verbose_name_plural = _('simple photos')

    def __str__(self):
        return _('Image #%(pk)s for entry %(app)s.%(model)s #%(entry_id)s') % {
            'pk': self.pk,
            'app': self.app_name,
            'model': self.model_name,
            'entry_id': self.instance_id,
        }

