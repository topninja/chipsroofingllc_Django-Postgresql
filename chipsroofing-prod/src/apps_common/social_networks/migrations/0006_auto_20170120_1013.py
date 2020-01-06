# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0005_auto_20170120_0957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialconfig',
            old_name='twitter_apikey',
            new_name='twitter_client_id',
        ),
        migrations.RenameField(
            model_name='socialconfig',
            old_name='twitter_secret',
            new_name='twitter_client_secret',
        ),
        migrations.AddField(
            model_name='socialconfig',
            name='linkedin_client_secret',
            field=models.CharField(max_length=48, blank=True, verbose_name='API Secret'),
        ),
        migrations.AddField(
            model_name='socialconfig',
            name='linkedin_client_id',
            field=models.CharField(max_length=48, blank=True, verbose_name='API Key'),
        ),
    ]
