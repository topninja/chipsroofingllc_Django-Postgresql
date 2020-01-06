# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_blogconfig_text_second'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='alt',
            field=models.CharField(verbose_name='Alt for SEO', help_text='for SEO', max_length=255, blank=True),
        ),
    ]
