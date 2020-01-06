# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0007_auto_20170413_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seoconfig',
            name='description',
            field=models.TextField(verbose_name='meta description', blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='description',
            field=models.TextField(verbose_name='meta description', blank=True, max_length=350),
        ),
    ]
