# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_blogpost_alt'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='background_alt',
            field=models.CharField(help_text='for SEO', max_length=255, verbose_name='Header image alt', blank=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='alt',
            field=models.CharField(help_text='for SEO', max_length=255, verbose_name='Preview alt', blank=True),
        ),
    ]
