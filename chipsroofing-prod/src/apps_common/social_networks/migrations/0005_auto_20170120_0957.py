# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0004_auto_20170120_0920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialconfig',
            old_name='twitter_app_id',
            new_name='twitter_apikey',
        ),
    ]
