# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.sprite_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(blank=True, verbose_name='title', max_length=128)),
                ('icon', libs.sprite_image.fields.SpriteImageField(default='icon', choices=[('icon', (0, -139)), ('icon', (-52, -139)), ('icon', (-100, -139)), ('icon', (-150, -139))], background='#FFFFFF', sprite='img/sprite.svg', verbose_name='icon', size=(50, 50))),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='order')),
            ],
            options={
                'verbose_name_plural': 'Free Estimate',
                'verbose_name': 'Free Estimate',
            },
        ),
        migrations.CreateModel(
            name='EstimateBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(serialize=False, to='attachable_blocks.AttachableBlock', auto_created=True, parent_link=True, primary_key=True)),
                ('header', models.CharField(blank=True, verbose_name='header', max_length=128)),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Estimate blocks',
                'verbose_name': 'Estimate block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.AddField(
            model_name='estimate',
            name='config',
            field=models.ForeignKey(default=True, to='blocks.EstimateBlock', related_name='estimate'),
        ),
    ]
