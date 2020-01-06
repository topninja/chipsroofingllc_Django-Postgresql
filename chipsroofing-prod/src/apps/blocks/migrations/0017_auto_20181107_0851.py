# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.videolink_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0016_remove_video_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videosblock',
            options={'verbose_name_plural': 'Video content block', 'verbose_name': 'Video content block'},
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=libs.videolink_field.fields.VideoLinkField(providers=set([]), blank=True, verbose_name='video'),
        ),
    ]
