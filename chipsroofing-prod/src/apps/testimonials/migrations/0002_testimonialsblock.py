# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
        ('testimonials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestimonialsBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='attachable_blocks.AttachableBlock', serialize=False, auto_created=True)),
                ('header', models.CharField(max_length=128, verbose_name='header', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Testimonials block',
                'verbose_name': 'Testimonials block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
