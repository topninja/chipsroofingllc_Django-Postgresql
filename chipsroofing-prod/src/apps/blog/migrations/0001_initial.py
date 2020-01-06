# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.stdimage.fields
import libs.autoslug
import django.utils.timezone
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('header', models.CharField(verbose_name='header', max_length=255)),
                ('microdata_author', models.CharField(verbose_name='author', max_length=255)),
                ('microdata_publisher_logo', models.ImageField(verbose_name='logo', upload_to='', storage=libs.storages.media_storage.MediaStorage('microdata'))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('header', models.CharField(verbose_name='header', max_length=255)),
                ('slug', libs.autoslug.AutoSlugField(unique=True, verbose_name='slug', populate_from='header')),
                ('note', models.TextField(verbose_name='note')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('date', models.DateTimeField(verbose_name='publication date', default=django.utils.timezone.now)),
                ('status', models.IntegerField(verbose_name='status', default=1, choices=[(1, 'Draft'), (2, 'Public')])),
                ('preview', libs.stdimage.fields.StdImageField(aspects=('normal',), upload_to='', storage=libs.storages.media_storage.MediaStorage('blog/preview'), variations={'mobile': {'size': (540, 300)}, 'normal': {'size': (900, 500)}, 'admin': {'size': (450, 250)}}, verbose_name='preview', blank=True, min_dimensions=(900, 500))),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'Post',
                'ordering': ('-date', '-id'),
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=255)),
                ('slug', libs.autoslug.AutoSlugField(unique=True, verbose_name='slug', populate_from='title')),
                ('sort_order', models.IntegerField(verbose_name='order', default=0)),
            ],
            options={
                'verbose_name': 'Tag',
                'ordering': ('sort_order',),
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(verbose_name='tags', related_name='posts', to='blog.Tag'),
        ),
    ]
