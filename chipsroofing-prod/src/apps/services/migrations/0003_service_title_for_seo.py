# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20181112_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='title_for_seo',
            field=models.CharField(default='', verbose_name='title for SEO', max_length=255),
            preserve_default=False,
        ),
    ]
