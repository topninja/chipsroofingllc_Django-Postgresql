# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_delete_aboutpageconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageconfig',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='mainpageconfig',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title', default=''),
            preserve_default=False,
        ),
    ]
