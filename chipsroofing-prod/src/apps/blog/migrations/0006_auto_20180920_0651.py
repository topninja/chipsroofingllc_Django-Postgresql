# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
from django.utils.timezone import utc
import libs.stdimage.fields
import datetime
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_blogconfig_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogconfig',
            name='background',
            field=libs.stdimage.fields.StdImageField(min_dimensions=(900, 0), verbose_name='Header image', null=True, variations={'tablet': {'size': (600, 0), 'crop': False}, 'admin': {'size': (300, 150), 'crop': True}, 'normal': {'size': (1090, 420), 'crop': True}, 'mobile': {'size': (290, 140), 'crop': False}}, storage=libs.storages.media_storage.MediaStorage('std_page/header'), upload_to='', blank=True, aspects=()),
        ),
        migrations.AddField(
            model_name='blogconfig',
            name='background_alt',
            field=models.CharField(help_text='for SEO', max_length=255, verbose_name='Header image alt', blank=True),
        ),
        migrations.AddField(
            model_name='blogconfig',
            name='text',
            field=ckeditor.fields.CKEditorUploadField(help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='Content block', blank=True),
        ),
        migrations.AddField(
            model_name='blogconfig',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2018, 9, 20, 10, 51, 23, 735706, tzinfo=utc), verbose_name='change date'),
            preserve_default=False,
        ),
    ]
