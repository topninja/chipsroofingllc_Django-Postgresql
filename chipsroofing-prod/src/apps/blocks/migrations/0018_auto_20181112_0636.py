# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.videolink_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0017_auto_20181107_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set(['youtube']), blank=True),
        ),
    ]
