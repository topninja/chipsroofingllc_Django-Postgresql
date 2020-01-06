# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_auto_20180914_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='visible',
            field=models.BooleanField(verbose_name='visible', default=True),
        ),
    ]
