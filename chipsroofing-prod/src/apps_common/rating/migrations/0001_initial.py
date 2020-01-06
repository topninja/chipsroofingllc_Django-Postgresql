# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import libs.range_field


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RatingVote',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(verbose_name='ip')),
                ('rating', libs.range_field.RangeField(verbose_name='vote', min_value=1, max_value=5)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, db_index=True, verbose_name='date')),
            ],
            options={
                'verbose_name': 'vote',
                'verbose_name_plural': 'votes',
            },
        ),
    ]
