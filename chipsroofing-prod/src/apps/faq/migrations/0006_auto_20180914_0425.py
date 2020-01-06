# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.sprite_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0005_faq_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='icon',
            field=libs.sprite_image.fields.SpriteImageField(verbose_name='icon', default='overlay-contract', sprite='img/sprite.svg', background='#FFFFFF', size=(50, 50), choices=[('overlay-contract', (0, -330)), ('overlay-insurance', (-45, -330)), ('overlay-warranty', (-90, -330)), ('overlay-materials', (-135, -330)), ('overlay-inspection', (-180, -330))]),
        ),
    ]
