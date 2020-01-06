# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20181101_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='background',
            field=libs.stdimage.fields.StdImageField(upload_to='', variations={'admin': {'size': (300, 150), 'crop': True}, 'tablet': {'size': (600, 0), 'crop': False}, 'normal': {'size': (1090, 420), 'crop': True}, 'mobile': {'size': (290, 140), 'crop': False}}, aspects=(), blank=True, null=True, min_dimensions=(1090, 420), storage=libs.storages.media_storage.MediaStorage('blog/header'), verbose_name='Header image'),
        ),
    ]
