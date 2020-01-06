# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0010_auto_20180920_0524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estimateblock',
            name='image',
        ),
    ]
