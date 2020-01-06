# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.file_field.fields
import libs.storages.media_storage
import libs.sprite_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
        ('blocks', '0002_estimateblock_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('image', libs.file_field.fields.ImageField(verbose_name='image', upload_to='', storage=libs.storages.media_storage.MediaStorage('blocks/partners'))),
                ('sort_order', models.PositiveIntegerField(verbose_name='order', default=0)),
            ],
            options={
                'verbose_name': 'Partners & Affiliations',
                'verbose_name_plural': 'Partners & Affiliations',
            },
        ),
        migrations.CreateModel(
            name='PartnersBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(to='attachable_blocks.AttachableBlock', serialize=False, auto_created=True, primary_key=True, parent_link=True)),
                ('header', models.CharField(verbose_name='header', blank=True, max_length=128)),
            ],
            options={
                'verbose_name': 'Estimate block',
                'verbose_name_plural': 'Estimate blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='icon',
            field=libs.sprite_image.fields.SpriteImageField(verbose_name='icon', sprite='img/sprite.svg', size=(50, 50), choices=[('icon-1', (0, -139)), ('icon-2', (-52, -139)), ('icon-3', (-100, -139)), ('icon-4', (-150, -139))], background='#FFFFFF', default='icon-1'),
        ),
        migrations.AddField(
            model_name='partners',
            name='config',
            field=models.ForeignKey(related_name='partners', to='blocks.PartnersBlock', default=True),
        ),
    ]
