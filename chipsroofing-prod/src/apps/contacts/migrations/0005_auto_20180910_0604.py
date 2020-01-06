# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_contactblock_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='openinghours',
            name='address',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='address',
        ),
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'address', 'verbose_name_plural': 'addresses'},
        ),
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(blank=True, verbose_name='phone', max_length=32),
        ),
        migrations.DeleteModel(
            name='OpeningHours',
        ),
        migrations.DeleteModel(
            name='PhoneNumber',
        ),
    ]
