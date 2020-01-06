# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0011_auto_20180921_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type_message',
            field=models.CharField(max_length=128, choices=[('contact', 'Contact Us'), ('estimate', 'Estimate')], default='contact', verbose_name='type message'),
        ),
    ]
