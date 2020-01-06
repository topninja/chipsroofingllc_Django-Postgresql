# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0017_auto_20181012_0714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address',
        ),
    ]
