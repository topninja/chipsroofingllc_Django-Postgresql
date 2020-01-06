# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutpageconfig',
            options={'verbose_name': 'Settings', 'default_permissions': ('change',)},
        ),
    ]
