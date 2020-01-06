# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0012_faq_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqconfig',
            name='text_second',
            field=ckeditor.fields.CKEditorUploadField(help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', blank=True, verbose_name='Content second block'),
        ),
    ]
