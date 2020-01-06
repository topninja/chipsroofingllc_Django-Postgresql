# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.sprite_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0006_auto_20180914_0425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='description',
        ),
        migrations.AlterField(
            model_name='faq',
            name='icon',
            field=libs.sprite_image.fields.SpriteImageField(verbose_name='icon', size=(44, 44), sprite='img/sprite.svg', choices=[('overlay-contract', (0, -330)), ('overlay-insurance', (-45, -330)), ('overlay-warranty', (-90, -330)), ('overlay-materials', (-135, -330)), ('overlay-inspection', (-180, -330))], background='#FFFFFF', default='overlay-contract'),
        ),
    ]
