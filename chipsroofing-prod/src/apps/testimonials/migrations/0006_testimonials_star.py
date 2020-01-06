# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import testimonials.models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0005_auto_20180925_0623'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonials',
            name='star',
            field=testimonials.models.IntegerRangeField(default=1),
            preserve_default=False,
        ),
    ]
