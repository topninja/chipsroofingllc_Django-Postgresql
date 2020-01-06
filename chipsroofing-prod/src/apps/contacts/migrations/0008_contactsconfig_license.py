# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0007_auto_20180910_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactsconfig',
            name='license',
            field=models.CharField(verbose_name='header', max_length=128, default=''),
            preserve_default=False,
        ),
    ]
