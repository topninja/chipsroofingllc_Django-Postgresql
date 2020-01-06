# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0003_auto_20170905_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachablereference',
            name='sort_order',
            field=models.IntegerField(verbose_name='sort order', default=0),
        ),
    ]
