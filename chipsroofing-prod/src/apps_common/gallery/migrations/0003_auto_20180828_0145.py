# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20170330_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryitembase',
            name='object_id',
            field=models.IntegerField(),
        ),
    ]
