# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0006_address_config'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='city',
        ),
        migrations.RemoveField(
            model_name='address',
            name='region',
        ),
        migrations.RemoveField(
            model_name='address',
            name='sort_order',
        ),
        migrations.RemoveField(
            model_name='address',
            name='zip',
        ),
    ]
