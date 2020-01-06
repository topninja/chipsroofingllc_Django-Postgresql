# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0003_auto_20180913_0809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testimonialspageconfig',
            name='description',
        ),
        migrations.RemoveField(
            model_name='testimonialspageconfig',
            name='title',
        ),
    ]
