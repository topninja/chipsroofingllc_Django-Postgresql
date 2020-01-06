# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0013_remove_address_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address',
            field=models.TextField(max_length=255, verbose_name='address', default=''),
            preserve_default=False,
        ),
    ]
