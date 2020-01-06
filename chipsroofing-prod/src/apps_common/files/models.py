import os
from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from libs.file_field.fields import FileField
from libs.storages.media_storage import MediaStorage


class PageFile(models.Model):
    """ Модель файла на страницу """
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')
    file = FileField(_('file'),
        storage=MediaStorage('files'),
        max_length=150,
    )
    name = models.CharField(_('name'),
        max_length=150,
        blank=True,
        help_text=_('If you leave it empty the file name will be used')
    )
    downloads = models.PositiveIntegerField(_('downloads count'), default=0)
    set_name = models.CharField(_('set name'), max_length=32, default='default')
    sort_order = models.PositiveIntegerField(_('sort order'))

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
        index_together = (('content_type', 'object_id', 'set_name'), )
        ordering = ('sort_order', )

    def __str__(self, *args, **kwargs):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = os.path.basename(self.file.path)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return resolve_url('files:download', file_id=self.pk)
