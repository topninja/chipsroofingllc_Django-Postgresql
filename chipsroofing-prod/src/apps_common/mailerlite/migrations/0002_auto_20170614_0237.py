# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='date_done',
            new_name='date_send',
        ),
        migrations.AlterField(
            model_name='campaign',
            name='date_send',
            field=models.DateTimeField(verbose_name='date send', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='remote_mail_id',
            field=models.BigIntegerField(default=0, editable=False, db_index=True,
                verbose_name='Mail ID in Mailerlite'),
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='date_started',
        ),
    ]
