# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20180925_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='background',
            field=libs.stdimage.fields.StdImageField(aspects=(), storage=libs.storages.media_storage.MediaStorage('blog/header'), upload_to='', verbose_name='Header image', blank=True, variations={'mobile': {'crop': False, 'size': (290, 140)}, 'admin': {'crop': True, 'size': (300, 150)}, 'tablet': {'crop': False, 'size': (600, 0)}, 'normal': {'crop': True, 'size': (1090, 420)}}, null=True, min_dimensions=(900, 0)),
        ),
    ]
