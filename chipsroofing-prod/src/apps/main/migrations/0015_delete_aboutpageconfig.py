# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20180913_0627'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AboutPageConfig',
        ),
    ]
