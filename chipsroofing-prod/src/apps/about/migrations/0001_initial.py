# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import libs.stdimage.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPageConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('background', libs.stdimage.fields.StdImageField(verbose_name='Header image', null=True, blank=True, upload_to='', aspects=(), min_dimensions=(900, 0), variations={'normal': {'size': (1090, 420), 'crop': True}, 'mobile': {'size': (290, 140), 'crop': False}, 'admin': {'size': (300, 150), 'crop': True}, 'tablet': {'size': (600, 0), 'crop': False}}, storage=libs.storages.media_storage.MediaStorage('std_page/header'))),
                ('background_alt', models.CharField(verbose_name='Header image alt', help_text='for SEO', blank=True, max_length=255)),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='Content block', help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', blank=True)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('title', models.CharField(verbose_name='header', blank=True, max_length=128)),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'About Us',
                'default_permissions': ('change',),
            },
        ),
    ]
