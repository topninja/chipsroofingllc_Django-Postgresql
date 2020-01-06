# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_auto_20180913_0809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutpageconfig',
            name='description',
        ),
        migrations.RemoveField(
            model_name='aboutpageconfig',
            name='title',
        ),
    ]
