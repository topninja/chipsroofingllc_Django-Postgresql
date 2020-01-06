# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.sprite_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0009_auto_20180913_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='icon',
            field=libs.sprite_image.fields.SpriteImageField(default='icon-1', choices=[('icon-1', (0, -380)), ('icon-2', (-34, -380)), ('icon-3', (-68, -380)), ('icon-4', (-102, -380))], sprite='img/sprite_bg.svg', background='#FFFFFF', verbose_name='icon', size=(34, 34)),
        ),
    ]
