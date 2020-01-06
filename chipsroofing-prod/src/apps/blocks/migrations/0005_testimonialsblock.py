# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
        ('blocks', '0004_auto_20180911_0809'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestimonialsBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to='attachable_blocks.AttachableBlock', auto_created=True)),
                ('header', models.CharField(verbose_name='header', max_length=128, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Testimonials',
                'verbose_name': 'Testimonial',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
    ]
