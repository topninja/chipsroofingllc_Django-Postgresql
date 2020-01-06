# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0003_socialconfig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialconfig',
            name='instagram_redirect_uri',
        ),
        migrations.AlterField(
            model_name='socialconfig',
            name='instagram_client_id',
            field=models.CharField(max_length=48, blank=True, verbose_name='Client ID'),
        ),
    ]
