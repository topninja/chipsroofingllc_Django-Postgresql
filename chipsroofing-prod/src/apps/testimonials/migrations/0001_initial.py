# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import ckeditor.fields
import libs.stdimage.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='header', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='order')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
            },
        ),
        migrations.CreateModel(
            name='TestimonialsPageConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('background', libs.stdimage.fields.StdImageField(aspects=(), verbose_name='Header image', null=True, min_dimensions=(900, 0), storage=libs.storages.media_storage.MediaStorage('std_page/header'), variations={'normal': {'size': (1090, 420), 'crop': True}, 'tablet': {'size': (600, 0), 'crop': False}, 'admin': {'size': (300, 150), 'crop': True}, 'mobile': {'size': (290, 140), 'crop': False}}, upload_to='', blank=True)),
                ('background_alt', models.CharField(help_text='for SEO', verbose_name='Header image alt', max_length=255, blank=True)),
                ('text', ckeditor.fields.CKEditorUploadField(help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', verbose_name='Content block', blank=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('title', models.CharField(max_length=128, verbose_name='header', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Testimonials',
            },
        ),
        migrations.AddField(
            model_name='testimonials',
            name='config',
            field=models.ForeignKey(related_name='testimonials', to='testimonials.TestimonialsPageConfig', default=True),
        ),
    ]
