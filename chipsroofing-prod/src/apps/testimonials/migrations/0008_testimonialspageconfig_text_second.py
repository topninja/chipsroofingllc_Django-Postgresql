# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0007_testimonials_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonialspageconfig',
            name='text_second',
            field=ckeditor.fields.CKEditorUploadField(help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', blank=True, verbose_name='Content second block'),
        ),
    ]
