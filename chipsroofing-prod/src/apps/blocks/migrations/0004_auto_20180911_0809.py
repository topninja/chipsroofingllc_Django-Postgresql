# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0003_auto_20180911_0653'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partnersblock',
            options={'verbose_name': 'Partners block', 'verbose_name_plural': 'Partners blocks'},
        ),
    ]
