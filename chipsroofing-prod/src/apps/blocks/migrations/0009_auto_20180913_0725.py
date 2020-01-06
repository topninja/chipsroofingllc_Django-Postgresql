# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
        ('blocks', '0008_auto_20180913_0714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examplesblock',
            name='attachableblock_ptr',
        ),
        migrations.DeleteModel(
            name='ExamplesBlock',
        ),
    ]
