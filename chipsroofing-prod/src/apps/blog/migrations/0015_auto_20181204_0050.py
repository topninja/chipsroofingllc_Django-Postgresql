# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20181115_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='background',
            field=libs.stdimage.fields.StdImageField(upload_to='', null=True, aspects=(), variations={'normal': {'crop': True, 'size': (1090, 420)}, 'tablet': {'crop': False, 'size': (600, 0)}, 'admin': {'crop': True, 'size': (300, 150)}, 'mobile': {'crop': False, 'size': (290, 140)}}, min_dimensions=(1090, 420), storage=libs.storages.media_storage.MediaStorage('blog/header'), verbose_name='Header image'),
        ),
    ]
