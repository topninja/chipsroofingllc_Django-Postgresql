# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0016_auto_20181004_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default='', verbose_name='city', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='region',
            field=models.CharField(blank=True, verbose_name='region', max_length=64),
        ),
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.CharField(blank=True, verbose_name='zip', max_length=32),
        ),
    ]
