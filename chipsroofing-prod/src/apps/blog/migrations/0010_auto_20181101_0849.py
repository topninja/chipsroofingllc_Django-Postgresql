# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20181101_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='preview',
            field=libs.stdimage.fields.StdImageField(verbose_name='preview', blank=True, min_dimensions=(300, 150), variations={'admin': {'size': (300, 150), 'crop': True}, 'mobile': {'size': (240, 180)}, 'normal': {'size': (350, 200)}}, aspects=('normal',), storage=libs.storages.media_storage.MediaStorage('blog/preview'), upload_to=''),
        ),
    ]
