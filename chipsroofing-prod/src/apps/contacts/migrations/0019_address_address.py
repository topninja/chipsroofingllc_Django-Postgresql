# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0018_remove_address_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=255, default='', verbose_name='address'),
            preserve_default=False,
        ),
    ]
