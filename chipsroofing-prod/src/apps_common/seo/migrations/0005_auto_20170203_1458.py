# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0004_auto_20161109_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='position',
            field=models.CharField(choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')], verbose_name='position', db_index=True, max_length=12),
        ),
    ]
