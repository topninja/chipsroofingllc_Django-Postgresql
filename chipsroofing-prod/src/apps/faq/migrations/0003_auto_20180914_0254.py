# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import libs.stdimage.fields
import ckeditor.fields
from django.utils.timezone import utc
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_remove_faqconfig_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqconfig',
            name='background',
            field=libs.stdimage.fields.StdImageField(storage=libs.storages.media_storage.MediaStorage('std_page/header'), null=True, verbose_name='Header image', upload_to='', variations={'tablet': {'crop': False, 'size': (600, 0)}, 'normal': {'crop': True, 'size': (1090, 420)}, 'admin': {'crop': True, 'size': (300, 150)}, 'mobile': {'crop': False, 'size': (290, 140)}}, min_dimensions=(900, 0), blank=True, aspects=()),
        ),
        migrations.AddField(
            model_name='faqconfig',
            name='background_alt',
            field=models.CharField(max_length=255, help_text='for SEO', blank=True, verbose_name='Header image alt'),
        ),
        migrations.AddField(
            model_name='faqconfig',
            name='text',
            field=ckeditor.fields.CKEditorUploadField(help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', blank=True, verbose_name='Content block'),
        ),
        migrations.AddField(
            model_name='faqconfig',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2018, 9, 14, 6, 54, 25, 401619, tzinfo=utc), verbose_name='change date'),
            preserve_default=False,
        ),
    ]
