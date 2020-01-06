# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
        ('examples', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamplesBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, parent_link=True, auto_created=True, to='attachable_blocks.AttachableBlock', serialize=False)),
                ('header', models.CharField(verbose_name='header', max_length=128, blank=True)),
            ],
            options={
                'verbose_name': 'Examples block',
                'verbose_name_plural': 'Examples block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
