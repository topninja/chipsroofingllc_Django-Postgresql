# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorize_net', '0001_initial'),
    ]

    operations = [
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
    ]
