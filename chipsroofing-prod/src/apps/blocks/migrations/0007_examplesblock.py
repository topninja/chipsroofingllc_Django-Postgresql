# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
        ('blocks', '0006_auto_20180912_0348'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamplesBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, to='attachable_blocks.AttachableBlock', primary_key=True, serialize=False, auto_created=True)),
                ('header', models.CharField(blank=True, verbose_name='header', max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Examples block',
                'verbose_name': 'Examples block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
