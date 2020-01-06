# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import libs.stdimage.fields
import libs.sprite_image.fields
import libs.storages.media_storage
import ckeditor.fields
import libs.autoslug


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('background', libs.stdimage.fields.StdImageField(blank=True, null=True, verbose_name='Header image', aspects=(), storage=libs.storages.media_storage.MediaStorage('std_page/header'), variations={'normal': {'crop': True, 'size': (1090, 420)}, 'tablet': {'crop': False, 'size': (600, 0)}, 'admin': {'crop': True, 'size': (300, 150)}, 'mobile': {'crop': False, 'size': (290, 140)}}, min_dimensions=(900, 0), upload_to='')),
                ('background_alt', models.CharField(blank=True, help_text='for SEO', verbose_name='Header image alt', max_length=255)),
                ('text', ckeditor.fields.CKEditorUploadField(blank=True, help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='Content block')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('slug', libs.autoslug.AutoSlugField(populate_from='title', verbose_name='slug', unique=True)),
                ('button_position', models.CharField(blank=True, choices=[('top-left', 'Top left'), ('top-middle', 'Top middle'), ('top-right', 'Top right'), ('bottom-left', 'Bottom left'), ('bottom-middle', 'Bottom middle'), ('bottom-right', 'Bottom right')], null=True, max_length=64, verbose_name='Button position')),
                ('icon', libs.sprite_image.fields.SpriteImageField(default='overlay-newroof', sprite='img/sprite.svg', background='#FFFFFF', verbose_name='icon', choices=[('overlay-newroof', (0, -232)), ('overlay-comerc-roof', (-45, -232)), ('overlay-resident-roof', (-93, -232)), ('overlay-roof-rep', (-138, -232)), ('overlay-siding', (-183, -232)), ('overlay-gutter', (-228, -232))], size=(44, 44))),
                ('visible', models.BooleanField(default=True, verbose_name='visible')),
                ('popup_image', libs.stdimage.fields.StdImageField(blank=True, null=True, verbose_name='Main popup image', aspects=(), storage=libs.storages.media_storage.MediaStorage('services_popup/img'), variations={'wide': {'size': (1920, 1720), 'stretch': True}, 'micro': {'size': (480, 430)}, 'mobile': {'size': (800, 750)}, 'desktop': {'size': (1400, 1250)}, 'admin': {'crop': True, 'size': (640, 480)}}, min_dimensions=(450, 0), upload_to='')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, verbose_name='parent service', to='services.Service', related_name='children')),
            ],
            options={
                'verbose_name_plural': 'Services',
                'ordering': ('sort_order',),
                'verbose_name': 'Service',
            },
        ),
        migrations.CreateModel(
            name='ServicesBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(to='attachable_blocks.AttachableBlock', parent_link=True, primary_key=True, serialize=False, auto_created=True)),
                ('header', models.CharField(blank=True, max_length=128, verbose_name='header')),
                ('image', libs.stdimage.fields.StdImageField(blank=True, null=True, verbose_name='Header image', aspects=(), storage=libs.storages.media_storage.MediaStorage('services_block/img'), variations={'normal': {'crop': True, 'size': (480, 300)}, 'tablet': {'crop': False, 'size': (480, 0)}, 'admin': {'crop': True, 'size': (300, 150)}}, min_dimensions=(450, 0), upload_to='')),
            ],
            options={
                'verbose_name_plural': 'Services block',
                'verbose_name': 'Services block',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='ServicesConfig',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('background', libs.stdimage.fields.StdImageField(blank=True, null=True, verbose_name='Header image', aspects=(), storage=libs.storages.media_storage.MediaStorage('std_page/header'), variations={'normal': {'crop': True, 'size': (1090, 420)}, 'tablet': {'crop': False, 'size': (600, 0)}, 'admin': {'crop': True, 'size': (300, 150)}, 'mobile': {'crop': False, 'size': (290, 140)}}, min_dimensions=(900, 0), upload_to='')),
                ('background_alt', models.CharField(blank=True, help_text='for SEO', verbose_name='Header image alt', max_length=255)),
                ('text', ckeditor.fields.CKEditorUploadField(blank=True, help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='Content block')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
    ]
