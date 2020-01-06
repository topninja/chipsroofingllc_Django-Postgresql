# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0004_auto_20170930_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachablereference',
            name='content_type',
            field=models.ForeignKey(related_name='+', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='attachablereference',
            name='object_id',
            field=models.IntegerField(),
        ),
    ]
