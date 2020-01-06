# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0020_remove_address_config'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'address', 'ordering': ('sort_order',), 'verbose_name_plural': 'addresses'},
        ),
        migrations.AddField(
            model_name='address',
            name='sort_order',
            field=models.PositiveIntegerField(default=1, verbose_name='order'),
            preserve_default=False,
        ),
    ]
