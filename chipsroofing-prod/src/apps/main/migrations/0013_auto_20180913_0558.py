# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_aboutpageconfig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examplesimageitem',
            name='galleryitembase_ptr',
        ),
        migrations.RemoveField(
            model_name='examplespageconfig',
            name='gallery',
        ),
        migrations.DeleteModel(
            name='Examples',
        ),
        migrations.DeleteModel(
            name='ExamplesImageItem',
        ),
        migrations.DeleteModel(
            name='ExamplesPageConfig',
        ),
    ]
