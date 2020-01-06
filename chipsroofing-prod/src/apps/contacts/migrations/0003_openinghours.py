# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.multiselect_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20170427_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('weekdays', libs.multiselect_field.fields.MultiSelectField(max_length=255, verbose_name='weekdays', choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('start_time', models.TimeField(verbose_name='from', null=True)),
                ('end_time', models.TimeField(verbose_name='to', null=True)),
                ('address', models.ForeignKey(related_name='hours', to='contacts.Address')),
            ],
            options={
                'verbose_name': 'opening hours sequence',
                'ordering': ('weekdays',),
                'verbose_name_plural': 'opening hours sequences',
            },
        ),
    ]
