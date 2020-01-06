# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import libs.autoslug


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', libs.autoslug.AutoSlugField(populate_from='title', unique=True, verbose_name='slug')),
                ('description', models.TextField(max_length=1024, verbose_name='short description')),
                ('text', ckeditor.fields.CKEditorUploadField(help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='text')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name': 'Faq',
                'verbose_name_plural': 'Faq',
            },
        ),
        migrations.CreateModel(
            name='FaqConfig',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('header', models.CharField(max_length=255, verbose_name='header')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'verbose_name': 'settings',
            },
        ),
    ]
