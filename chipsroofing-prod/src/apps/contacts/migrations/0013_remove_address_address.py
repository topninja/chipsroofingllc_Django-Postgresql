# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0012_auto_20180921_0756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address',
        ),
    ]
