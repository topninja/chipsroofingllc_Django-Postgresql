# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0010_message_type_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type_message',
            field=models.CharField(choices=[('contact', 'Contact Us'), ('estimate', 'Estimate')], default='contact', max_length=128, verbose_name='name'),
        ),
    ]
