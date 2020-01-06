# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0015_auto_20181107_0629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='title',
        ),
    ]
