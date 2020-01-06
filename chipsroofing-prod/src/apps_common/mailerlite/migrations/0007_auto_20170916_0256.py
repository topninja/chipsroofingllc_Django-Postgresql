# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0006_auto_20170915_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='date_subscribe',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date subscribe', editable=False),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='date_updated',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date updated', editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='clicked',
            field=models.PositiveIntegerField(default=0, verbose_name='clicked', editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='date_unsubscribe',
            field=models.DateTimeField(editable=False, verbose_name='date unsubscribe', null=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='opened',
            field=models.PositiveIntegerField(default=0, verbose_name='opened', editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='sent',
            field=models.PositiveIntegerField(default=0, verbose_name='sent', editable=False),
        ),
    ]
