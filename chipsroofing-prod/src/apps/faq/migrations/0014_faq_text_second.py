# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0013_faqconfig_text_second'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='text_second',
            field=ckeditor.fields.CKEditorUploadField(blank=True, verbose_name='Content second block', help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>'),
        ),
    ]
