# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import libs.storages.media_storage
import gallery.fields
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20180828_0145'),
        ('main', '0004_auto_20180911_0902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Examples',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ExamplesImageItem',
            fields=[
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, parent_link=True, to='gallery.GalleryItemBase', auto_created=True, primary_key=True)),
                ('image', gallery.fields.GalleryImageField(verbose_name='image', upload_to=gallery.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage())),
                ('image_crop', models.CharField(verbose_name='stored_crop', max_length=32, editable=False, blank=True)),
                ('image_alt', models.CharField(verbose_name='alt', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'image item',
                'verbose_name_plural': 'image items',
                'ordering': ('object_id', 'sort_order', 'created'),
                'abstract': False,
                'default_permissions': (),
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='ExamplesPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=128, blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('gallery', gallery.fields.GalleryField(to='main.Examples', on_delete=django.db.models.deletion.SET_NULL, verbose_name='gallery', null=True)),
            ],
            options={
                'verbose_name': 'Examples',
                'default_permissions': ('change',),
            },
        ),
    ]
