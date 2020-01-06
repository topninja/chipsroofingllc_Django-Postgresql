# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0005_auto_20170915_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='status',
        ),
        migrations.AddField(
            model_name='group',
            name='bounced',
            field=models.PositiveIntegerField(verbose_name='bounced', default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='active',
            field=models.PositiveIntegerField(verbose_name='active', default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='clicked',
            field=models.PositiveIntegerField(verbose_name='clicked', default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='date_updated',
            field=models.DateTimeField(verbose_name='date updated', default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='opened',
            field=models.PositiveIntegerField(verbose_name='opened', default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='remote_id',
            field=models.BigIntegerField(db_index=True, default=0, verbose_name='ID in Mailerlite'),
        ),
        migrations.AlterField(
            model_name='group',
            name='sent',
            field=models.PositiveIntegerField(verbose_name='sent', default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='total',
            field=models.PositiveIntegerField(verbose_name='total', default=0, editable=False),
        ),
    ]
