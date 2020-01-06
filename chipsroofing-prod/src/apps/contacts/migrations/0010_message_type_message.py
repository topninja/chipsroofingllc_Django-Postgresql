# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_auto_20180918_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='type_message',
            field=models.CharField(choices=[('Contact Us', 'contact'), ('Estimate', 'estimate')], verbose_name='name', max_length=128, default='contact'),
        ),
    ]
