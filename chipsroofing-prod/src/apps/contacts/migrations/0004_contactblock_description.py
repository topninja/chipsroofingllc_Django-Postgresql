# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_openinghours'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactblock',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
    ]
