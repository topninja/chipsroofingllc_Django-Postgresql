# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0008_faqblock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ('sort_order',), 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.RemoveField(
            model_name='faqconfig',
            name='header',
        ),
    ]
