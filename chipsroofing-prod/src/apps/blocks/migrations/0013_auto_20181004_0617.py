# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.sprite_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0012_estimateblock_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='icon',
            field=libs.sprite_image.fields.SpriteImageField(sprite='img/sprite.svg', size=(34, 34), choices=[('icon-1', (0, -380)), ('icon-2', (-34, -380)), ('icon-3', (-68, -380)), ('icon-4', (-102, -380))], verbose_name='icon', background='#FFFFFF', default='icon-1'),
        ),
    ]
