# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20180913_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examplespageconfig',
            name='background',
            field=libs.stdimage.fields.StdImageField(verbose_name='background', min_dimensions=(900, 0), null=True, storage=libs.storages.media_storage.MediaStorage('std_page/header'), blank=True, aspects=(), upload_to='', variations={'tablet': {'crop': False, 'size': (600, 0)}, 'admin': {'crop': True, 'size': (300, 150)}, 'mobile': {'crop': False, 'size': (290, 140)}, 'normal': {'crop': True, 'size': (1090, 420)}}),
        ),
    ]
