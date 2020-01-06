# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0021_auto_20181015_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='url',
            field=models.URLField(verbose_name='directions link', blank=True),
        ),
    ]
