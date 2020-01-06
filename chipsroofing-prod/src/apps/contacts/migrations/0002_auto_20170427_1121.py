# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='referer',
            field=models.CharField(editable=False, verbose_name='from page', blank=True, max_length=512),
        ),
    ]
