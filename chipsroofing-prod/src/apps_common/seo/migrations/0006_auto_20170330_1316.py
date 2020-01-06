# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0005_auto_20170203_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seodata',
            name='noindex',
            field=models.BooleanField(verbose_name='noindex', default=False, help_text='text on the page will not be indexed'),
        ),
    ]
