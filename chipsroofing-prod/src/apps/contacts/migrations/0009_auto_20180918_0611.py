# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_contactsconfig_license'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactsconfig',
            name='license',
            field=models.CharField(verbose_name='license', max_length=128),
        ),
    ]
