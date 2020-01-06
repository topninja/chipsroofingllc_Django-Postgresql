# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.file_field.fields
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('ckeditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagefile',
            name='file',
            field=libs.file_field.fields.FileField(blank=True, storage=libs.storages.media_storage.MediaStorage('page_files'), upload_to=ckeditor.models.split_by_dirs, verbose_name='file'),
        ),
    ]
