# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
        ('blog', '0003_auto_20180918_0837'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, to='attachable_blocks.AttachableBlock', parent_link=True, serialize=False, primary_key=True)),
                ('header', models.CharField(max_length=128, verbose_name='header', blank=True)),
            ],
            options={
                'verbose_name': 'Blog block',
                'verbose_name_plural': 'Blog blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
