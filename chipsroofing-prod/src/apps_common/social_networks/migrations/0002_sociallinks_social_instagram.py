# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sociallinks',
            name='social_instagram',
            field=models.URLField(verbose_name='instagram', blank=True, max_length=255),
        ),
    ]
