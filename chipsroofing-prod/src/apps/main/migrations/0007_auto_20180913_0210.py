# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import libs.storages.media_storage
import libs.stdimage.fields
from django.utils.timezone import utc
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_examplespageconfig_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='examplespageconfig',
            name='background',
            field=libs.stdimage.fields.StdImageField(aspects=(), storage=libs.storages.media_storage.MediaStorage('std_page/header'), upload_to='', variations={'admin': {'crop': True, 'size': (200, 150)}, 'normal': {'crop': True, 'size': (1090, 420)}, 'tablet': {'crop': False, 'size': (600, 0)}, 'mobile': {'crop': False, 'size': (290, 140)}}, null=True, verbose_name='background', blank=True, min_dimensions=(900, 0)),
        ),
        migrations.AddField(
            model_name='examplespageconfig',
            name='background_alt',
            field=models.CharField(help_text='for SEO', max_length=255, blank=True, verbose_name='background alt'),
        ),
        migrations.AddField(
            model_name='examplespageconfig',
            name='text',
            field=ckeditor.fields.CKEditorUploadField(help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='Content', blank=True),
        ),
        migrations.AddField(
            model_name='examplespageconfig',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 13, 6, 10, 4, 589952, tzinfo=utc), verbose_name='change date', auto_now=True),
            preserve_default=False,
        ),
    ]
