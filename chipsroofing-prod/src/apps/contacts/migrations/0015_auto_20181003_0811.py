# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0014_address_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type_message',
            field=models.CharField(default='contact', choices=[('btn-blue', 'Contact Us'), ('btn-red', 'Estimate')], verbose_name='type message', max_length=128),
        ),
    ]
