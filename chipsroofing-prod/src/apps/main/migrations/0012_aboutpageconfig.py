# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import libs.storages.media_storage
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20180913_0329'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPageConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('background', libs.stdimage.fields.StdImageField(variations={'normal': {'crop': True, 'size': (1090, 420)}, 'admin': {'crop': True, 'size': (300, 150)}, 'tablet': {'crop': False, 'size': (600, 0)}, 'mobile': {'crop': False, 'size': (290, 140)}}, aspects=(), blank=True, null=True, verbose_name='Header image', upload_to='', min_dimensions=(900, 0), storage=libs.storages.media_storage.MediaStorage('std_page/header'))),
                ('background_alt', models.CharField(verbose_name='Header image alt', help_text='for SEO', max_length=255, blank=True)),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='Content block', help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', blank=True)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
                ('title', models.CharField(verbose_name='header', max_length=128, blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'About Us',
                'default_permissions': ('change',),
            },
        ),
    ]
