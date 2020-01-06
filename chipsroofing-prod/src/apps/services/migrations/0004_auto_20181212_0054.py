# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_service_title_for_seo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='button_position',
            field=models.CharField(verbose_name='Button position', choices=[('top-left', 'Top left'), ('top-middle', 'Top middle'), ('top-right', 'Top right'), ('bottom-left', 'Bottom left'), ('bottom-middle', 'Bottom middle'), ('bottom-right', 'Bottom right')], blank=True, unique=True, max_length=64, null=True),
        ),
    ]
