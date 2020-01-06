# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0011_remove_estimateblock_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimateblock',
            name='image',
            field=libs.stdimage.fields.StdImageField(null=True, storage=libs.storages.media_storage.MediaStorage('blocks/estimate'), upload_to='', variations={'mobile': {'size': (290, 376), 'crop': False}, 'admin': {'size': (300, 200), 'crop': True}, 'normal': {'size': (1090, 380), 'crop': True}, 'tablet': {'size': (600, 0), 'crop': False}}, verbose_name='background', min_dimensions=(450, 0), aspects=(), blank=True),
        ),
    ]
