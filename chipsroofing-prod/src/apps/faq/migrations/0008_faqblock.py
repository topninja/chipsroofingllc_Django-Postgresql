# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
        ('faq', '0007_auto_20180914_0513'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(to='attachable_blocks.AttachableBlock', serialize=False, auto_created=True, parent_link=True, primary_key=True)),
                ('header', models.CharField(max_length=128, blank=True, verbose_name='header')),
            ],
            options={
                'verbose_name': 'FAQ block',
                'verbose_name_plural': 'FAQs block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
