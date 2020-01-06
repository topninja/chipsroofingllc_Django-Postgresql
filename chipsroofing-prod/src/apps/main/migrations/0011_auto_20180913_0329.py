# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import libs.stdimage.fields
import datetime
import ckeditor.fields
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20180913_0328'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonialspageconfig',
            name='background',
            field=libs.stdimage.fields.StdImageField(verbose_name='Header image', variations={'admin': {'crop': True, 'size': (300, 150)}, 'mobile': {'crop': False, 'size': (290, 140)}, 'tablet': {'crop': False, 'size': (600, 0)}, 'normal': {'crop': True, 'size': (1090, 420)}}, storage=libs.storages.media_storage.MediaStorage('std_page/header'), min_dimensions=(900, 0), blank=True, null=True, upload_to='', aspects=()),
        ),
        migrations.AddField(
            model_name='testimonialspageconfig',
            name='background_alt',
            field=models.CharField(help_text='for SEO', max_length=255, verbose_name='Header image alt', blank=True),
        ),
        migrations.AddField(
            model_name='testimonialspageconfig',
            name='text',
            field=ckeditor.fields.CKEditorUploadField(help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='Content block', blank=True),
        ),
        migrations.AddField(
            model_name='testimonialspageconfig',
            name='updated',
            field=models.DateTimeField(verbose_name='change date', auto_now=True, default=datetime.datetime(2018, 9, 13, 7, 29, 25, 929464, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
