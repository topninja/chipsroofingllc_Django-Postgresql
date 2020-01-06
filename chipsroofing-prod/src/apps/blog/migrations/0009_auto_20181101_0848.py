# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_blogpost_background'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='preview',
            field=libs.stdimage.fields.StdImageField(verbose_name='preview', aspects=('normal',), min_dimensions=(300, 150), blank=True, variations={'admin': {'size': (300, 150)}, 'normal': {'size': (350, 200)}, 'mobile': {'size': (240, 180)}}, upload_to='', storage=libs.storages.media_storage.MediaStorage('blog/preview')),
        ),
    ]
