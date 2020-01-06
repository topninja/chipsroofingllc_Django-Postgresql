# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0002_auto_20170614_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='date_created',
            field=models.DateTimeField(editable=False, verbose_name='date subscribed', default=django.utils.timezone.now),
        ),
    ]
