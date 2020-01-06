# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0010_auto_20180918_0517'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqconfig',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='faqconfig',
            name='title',
            field=models.CharField(verbose_name='title', default='', max_length=255),
            preserve_default=False,
        ),
    ]
