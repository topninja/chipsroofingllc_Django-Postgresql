# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.models
import libs.stdimage.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0002_auto_20160916_0501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagephoto',
            name='photo',
            field=libs.stdimage.fields.StdImageField(upload_to=ckeditor.models.split_by_dirs, min_dimensions=(800, 450), storage=libs.storages.media_storage.MediaStorage('page_photos'), aspects='normal', blank=True, verbose_name='image', variations={'wide': {'size': (1024, 576), 'quality': 88}, 'normal': {'size': (800, 450)}, 'mobile': {'size': (480, 270)}}),
        ),
    ]
