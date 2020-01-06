# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0006_testimonials_star'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonials',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='visible'),
        ),
    ]
