# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0015_auto_20181003_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type_message',
            field=models.CharField(verbose_name='type message', choices=[('btn-popup-contact', 'Contact Us'), ('btn-popup-estimate', 'Estimate')], max_length=128, default='contact'),
        ),
    ]
