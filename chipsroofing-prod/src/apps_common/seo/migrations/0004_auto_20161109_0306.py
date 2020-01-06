# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0003_auto_20160916_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seodata',
            name='description',
            field=models.TextField(verbose_name='meta description', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='keywords',
            field=models.TextField(verbose_name='meta keywords', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='og_title',
            field=models.CharField(verbose_name='header', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='seodata',
            name='title',
            field=models.CharField(verbose_name='meta title', max_length=128, blank=True),
        ),
    ]
