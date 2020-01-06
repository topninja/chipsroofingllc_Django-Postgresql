# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0022_address_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='email',
            field=models.EmailField(max_length=254, blank=True, verbose_name='e-mail'),
        ),
        migrations.AddField(
            model_name='address',
            name='fax',
            field=models.CharField(max_length=255, blank=True, verbose_name='fax'),
        ),
    ]
