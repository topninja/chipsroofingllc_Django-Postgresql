# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0002_auto_20170607_0345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachablereference',
            name='ajax',
            field=models.BooleanField(help_text='load block via AJAX', verbose_name='AJAX', default=False),
        ),
    ]
