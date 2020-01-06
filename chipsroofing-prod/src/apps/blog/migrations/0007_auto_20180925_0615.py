# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180920_0651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogconfig',
            name='header',
        ),
        migrations.AddField(
            model_name='blogconfig',
            name='title',
            field=models.CharField(default='', max_length=255, verbose_name='title'),
            preserve_default=False,
        ),
    ]
