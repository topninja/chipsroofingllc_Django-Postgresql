# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0006_auto_20170120_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialconfig',
            name='facebook_client_id',
            field=models.CharField(verbose_name='App ID', max_length=48, blank=True),
        ),
        migrations.AddField(
            model_name='socialconfig',
            name='facebook_client_secret',
            field=models.CharField(verbose_name='App Secret', max_length=64, blank=True),
        ),
    ]
