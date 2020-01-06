# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_testimonialspageconfig'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testimonialspageconfig',
            options={'verbose_name': 'Testimonials', 'default_permissions': ('change',)},
        ),
    ]
