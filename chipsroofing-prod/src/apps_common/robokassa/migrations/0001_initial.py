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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('inv_id', models.PositiveIntegerField(verbose_name='InvId', blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='status', choices=[(1, 'Message'), (2, 'Success'), (3, 'Error'), (4, 'Exception')])),
                ('message', models.TextField(verbose_name='message')),
                ('request', models.TextField(verbose_name='request')),
                ('created', models.DateTimeField(editable=False, verbose_name='create date', default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'log message',
                'ordering': ('-created',),
                'verbose_name_plural': 'log messages',
            },
        ),
    ]
