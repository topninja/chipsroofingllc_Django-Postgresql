# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20180913_0558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testimonials',
            name='config',
        ),
        migrations.DeleteModel(
            name='Testimonials',
        ),
        migrations.DeleteModel(
            name='TestimonialsPageConfig',
        ),
    ]
