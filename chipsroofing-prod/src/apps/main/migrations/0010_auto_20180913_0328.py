# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import libs.stdimage.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20180913_0213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testimonialspageconfig',
            name='updated',
        ),
        migrations.AlterField(
            model_name='examplespageconfig',
            name='background',
            field=libs.stdimage.fields.StdImageField(min_dimensions=(900, 0), null=True, storage=libs.storages.media_storage.MediaStorage('std_page/header'), variations={'admin': {'crop': True, 'size': (300, 150)}, 'mobile': {'crop': False, 'size': (290, 140)}, 'tablet': {'crop': False, 'size': (600, 0)}, 'normal': {'crop': True, 'size': (1090, 420)}}, verbose_name='Header image', blank=True, aspects=(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='examplespageconfig',
            name='background_alt',
            field=models.CharField(help_text='for SEO', verbose_name='Header image alt', blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='examplespageconfig',
            name='text',
            field=ckeditor.fields.CKEditorUploadField(help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='Content block', blank=True),
        ),
    ]
