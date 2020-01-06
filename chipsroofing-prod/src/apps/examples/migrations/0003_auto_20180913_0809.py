# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0002_examplesblock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='examplespageconfig',
            options={'default_permissions': ('change',), 'verbose_name': 'Settings'},
        ),
    ]
