# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0002_testimonialsblock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testimonialspageconfig',
            options={'verbose_name': 'Settings', 'default_permissions': ('change',)},
        ),
    ]
