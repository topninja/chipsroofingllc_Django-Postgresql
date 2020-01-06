# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0011_auto_20180925_0621'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
    ]
