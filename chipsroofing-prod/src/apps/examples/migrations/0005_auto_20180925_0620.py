# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0004_auto_20180918_0538'),
    ]

    operations = [
        migrations.AddField(
            model_name='examplespageconfig',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='examplespageconfig',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title', default=''),
            preserve_default=False,
        ),
    ]
