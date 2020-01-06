# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.file_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimateblock',
            name='image',
            field=libs.file_field.fields.ImageField(default='', upload_to='', storage=libs.storages.media_storage.MediaStorage('blocks/estimate'), verbose_name='image'),
            preserve_default=False,
        ),
    ]
