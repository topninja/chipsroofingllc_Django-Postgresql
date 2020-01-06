# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'verbose_name_plural': 'log messages', 'default_permissions': ('delete',), 'verbose_name': 'log message', 'ordering': ('-created',)},
        ),
        migrations.RenameField(
            model_name='log',
            old_name='message',
            new_name='msg_body',
        ),
        migrations.RemoveField(
            model_name='log',
            name='request',
        ),
        migrations.AddField(
            model_name='log',
            name='request_get',
            field=models.TextField(verbose_name='GET', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='log',
            name='request_ip',
            field=models.GenericIPAddressField(verbose_name='IP', default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='log',
            name='request_post',
            field=models.TextField(verbose_name='POST', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='log',
            name='inv_id',
            field=models.BigIntegerField(blank=True, verbose_name='invoice', null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='status',
            field=models.PositiveSmallIntegerField(verbose_name='status', choices=[(1, 'Info'), (2, 'Success'), (3, 'Error'), (4, 'Exception')]),
        ),
    ]
