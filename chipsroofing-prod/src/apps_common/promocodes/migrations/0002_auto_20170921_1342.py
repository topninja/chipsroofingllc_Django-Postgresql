# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promocodes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promosettings',
            name='subscribe_email',
        ),
        migrations.RemoveField(
            model_name='promosettings',
            name='subscribe_note',
        ),
        migrations.RemoveField(
            model_name='promosettings',
            name='subscribe_parameter',
        ),
        migrations.RemoveField(
            model_name='promosettings',
            name='subscribe_strategy_name',
        ),
    ]
