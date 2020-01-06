# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_examples_examplesimageitem_examplespageconfig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examplespageconfig',
            name='updated',
        ),
    ]
