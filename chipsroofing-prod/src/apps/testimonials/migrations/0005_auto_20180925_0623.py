# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0004_auto_20180925_0606'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonialspageconfig',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='testimonialspageconfig',
            name='title',
            field=models.CharField(verbose_name='title', max_length=255, default=''),
            preserve_default=False,
        ),
    ]
