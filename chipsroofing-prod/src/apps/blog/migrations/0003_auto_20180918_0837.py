# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180907_0537'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogconfig',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='preview',
            field=libs.stdimage.fields.StdImageField(storage=libs.storages.media_storage.MediaStorage('blog/preview'), blank=True, verbose_name='preview', variations={'admin': {'size': (350, 200)}, 'mobile': {'size': (240, 180)}, 'normal': {'size': (350, 200)}}, upload_to='', min_dimensions=(300, 150), aspects=('normal',)),
        ),
    ]
