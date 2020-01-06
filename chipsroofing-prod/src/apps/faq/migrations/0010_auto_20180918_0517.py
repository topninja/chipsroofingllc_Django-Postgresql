# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0009_auto_20180917_0441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='text',
            field=ckeditor.fields.CKEditorUploadField(blank=True, help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='text'),
        ),
    ]
