# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gallery.fields
import libs.stdimage.fields
import ckeditor.fields
import django.db.models.deletion
import gallery.models
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20180828_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Examples',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('galleryitembase_ptr', models.OneToOneField(serialize=False, primary_key=True, to='gallery.GalleryItemBase', auto_created=True, parent_link=True)),
                ('image', gallery.fields.GalleryImageField(upload_to=gallery.models.generate_filepath, storage=libs.storages.media_storage.MediaStorage(), verbose_name='image')),
                ('image_crop', models.CharField(verbose_name='stored_crop', blank=True, editable=False, max_length=32)),
                ('image_alt', models.CharField(verbose_name='alt', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'image item',
                'default_permissions': (),
                'verbose_name_plural': 'image items',
                'abstract': False,
                'ordering': ('object_id', 'sort_order', 'created'),
            },
            bases=('gallery.galleryitembase',),
        ),
        migrations.CreateModel(
            name='ExamplesPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('background', libs.stdimage.fields.StdImageField(min_dimensions=(900, 0), aspects=(), upload_to='', null=True, blank=True, storage=libs.storages.media_storage.MediaStorage('std_page/header'), variations={'mobile': {'crop': False, 'size': (290, 140)}, 'tablet': {'crop': False, 'size': (600, 0)}, 'admin': {'crop': True, 'size': (300, 150)}, 'normal': {'crop': True, 'size': (1090, 420)}}, verbose_name='Header image')),
                ('background_alt', models.CharField(verbose_name='Header image alt', max_length=255, blank=True, help_text='for SEO')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='Content block', blank=True, help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('title', models.CharField(verbose_name='title', blank=True, max_length=128)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('gallery', gallery.fields.GalleryField(to='examples.Examples', on_delete=django.db.models.deletion.SET_NULL, null=True, verbose_name='gallery')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Examples',
            },
        ),
    ]
