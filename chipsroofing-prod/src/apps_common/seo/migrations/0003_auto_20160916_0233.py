# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0002_redirect_last_usage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seodata',
            name='header',
        ),
        migrations.RemoveField(
            model_name='seodata',
            name='text',
        ),
    ]
