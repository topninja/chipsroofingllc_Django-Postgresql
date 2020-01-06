# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.stdimage.fields
import libs.storages.media_storage
import ckeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('file', models.FileField(blank=True, verbose_name='file', upload_to=ckeditor.models.split_by_dirs, storage=libs.storages.media_storage.MediaStorage('page_files'))),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'page file',
                'verbose_name_plural': 'page files',
            },
        ),
        migrations.CreateModel(
            name='PagePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, min_dimensions=(1024, 768), storage=libs.storages.media_storage.MediaStorage('page_photos'), aspects='normal', variations={'mobile': {'crop': False, 'max_width': 480, 'size': (0, 0)}, 'wide': {'quality': 95, 'crop': False, 'max_width': 1440, 'size': (0, 0)}, 'normal': {'crop': False, 'max_width': 800, 'size': (0, 0)}}, verbose_name='image', upload_to=ckeditor.models.split_by_dirs)),
                ('photo_crop', models.CharField(blank=True, verbose_name='crop', editable=False, max_length=32)),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'page photo',
                'verbose_name_plural': 'page photos',
            },
        ),
        migrations.CreateModel(
            name='SimplePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('app_name', models.CharField(blank=True, verbose_name='application', max_length=30)),
                ('model_name', models.CharField(blank=True, verbose_name='model', max_length=30)),
                ('instance_id', models.IntegerField(default=0, verbose_name='entry id', db_index=True)),
                ('photo', libs.stdimage.fields.StdImageField(blank=True, storage=libs.storages.media_storage.MediaStorage('simple_photos'), aspects=(), variations={'mobile': {'crop': False, 'max_width': 512, 'size': (0, 0)}}, max_source_dimensions=(3072, 3072), verbose_name='image', upload_to=ckeditor.models.split_by_dirs)),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'simple photo',
                'verbose_name_plural': 'simple photos',
            },
        ),
    ]
