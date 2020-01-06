# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20180913_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examplespageconfig',
            name='background',
            field=libs.stdimage.fields.StdImageField(null=True, verbose_name='background', storage=libs.storages.media_storage.MediaStorage('std_page/header'), upload_to='', aspects=(), variations={'mobile': {'size': (290, 140), 'crop': False}, 'normal': {'size': (1090, 420), 'crop': True}, 'tablet': {'size': (600, 0), 'crop': False}, 'admin': {'size': (300, 0), 'crop': True}}, min_dimensions=(900, 0), blank=True),
        ),
    ]
