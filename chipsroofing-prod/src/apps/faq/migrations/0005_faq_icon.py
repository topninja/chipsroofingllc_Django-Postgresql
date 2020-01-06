# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.sprite_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0004_faq_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='icon',
            field=libs.sprite_image.fields.SpriteImageField(default='overlay-contract-1', background='#FFFFFF', sprite='img/sprite.svg', choices=[('overlay-contract-1', (0, -139)), ('overlay-insurance-2', (-52, -139)), ('overlay-warranty-3', (-100, -139)), ('overlay-materials', (-150, -139)), ('overlay-inspection', (-150, -139))], size=(50, 50), verbose_name='icon'),
        ),
    ]
