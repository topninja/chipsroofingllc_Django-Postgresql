# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0019_address_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='config',
        ),
    ]
