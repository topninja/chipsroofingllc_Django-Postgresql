# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0006_auto_20170330_1316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='counter',
            options={'ordering': ('sort_order',), 'verbose_name_plural': 'counters', 'verbose_name': 'counter'},
        ),
        migrations.AddField(
            model_name='counter',
            name='sort_order',
            field=models.IntegerField(default=0, verbose_name='order'),
        ),
    ]
