# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('inv_id', models.PositiveIntegerField(blank=True, verbose_name='InvId', null=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', choices=[(1, 'Message'), (2, 'Success'), (3, 'Error'), (4, 'Exception')])),
                ('message', models.TextField(verbose_name='message')),
                ('request', models.TextField(verbose_name='request')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='create date', editable=False)),
            ],
            options={
                'verbose_name': 'log message',
                'ordering': ('-created',),
                'verbose_name_plural': 'log messages',
            },
        ),
    ]
