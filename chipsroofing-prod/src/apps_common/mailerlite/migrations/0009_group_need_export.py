# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0008_auto_20170918_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='need_export',
            field=models.BooleanField(verbose_name='need export', default=False),
        ),
    ]
