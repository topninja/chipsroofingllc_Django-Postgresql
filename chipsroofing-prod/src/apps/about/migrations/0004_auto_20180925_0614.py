# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0003_auto_20180925_0540'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutpageconfig',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='aboutpageconfig',
            name='title',
            field=models.CharField(default='', verbose_name='title', max_length=255),
            preserve_default=False,
        ),
    ]
