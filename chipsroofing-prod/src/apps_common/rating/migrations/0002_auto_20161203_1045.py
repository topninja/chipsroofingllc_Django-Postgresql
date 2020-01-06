# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ratingvote',
            options={'verbose_name': 'vote', 'ordering': ('-date',), 'verbose_name_plural': 'votes'},
        ),
    ]
