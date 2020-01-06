# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0005_testimonialsblock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testimonialsblock',
            options={'verbose_name_plural': 'Testimonials block', 'verbose_name': 'Testimonials block'},
        ),
    ]
