# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Robots',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('text', models.TextField(blank=True, verbose_name='text')),
            ],
            options={
                'managed': False,
                'default_permissions': (),
                'verbose_name': 'file',
                'verbose_name_plural': 'robots.txt',
            },
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('label', models.CharField(verbose_name='label', max_length=128)),
                ('position', models.CharField(verbose_name='position', max_length=12, choices=[('head', 'Inside <head>'), ('body_top', 'Start of <body>'), ('body_bottom', 'End of <body>')])),
                ('content', models.TextField(verbose_name='content')),
            ],
            options={
                'verbose_name': 'counter',
                'verbose_name_plural': 'counters',
            },
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('old_path', models.CharField(verbose_name='redirect from', unique=True, help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'.", max_length=200)),
                ('new_path', models.CharField(blank=True, verbose_name='redirect to', help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'.", max_length=200)),
                ('permanent', models.BooleanField(default=True, verbose_name='permanent')),
                ('note', models.TextField(blank=True, verbose_name='note', max_length=255)),
                ('created', models.DateField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
            ],
            options={
                'verbose_name': 'redirect',
                'ordering': ('old_path',),
                'verbose_name_plural': 'redirects',
            },
        ),
        migrations.CreateModel(
            name='SeoConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(blank=True, verbose_name='meta title', max_length=128)),
                ('keywords', models.TextField(blank=True, verbose_name='meta keywords', max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='meta description', max_length=255)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Defaults',
            },
        ),
        migrations.CreateModel(
            name='SeoData',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(blank=True, verbose_name='title', max_length=128)),
                ('keywords', models.TextField(blank=True, verbose_name='keywords', max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='description', max_length=255)),
                ('canonical', models.URLField(blank=True, verbose_name='canonical URL')),
                ('noindex', models.BooleanField(default=False, verbose_name='noindex', help_text='the text on the page will not be indexed')),
                ('og_title', models.CharField(blank=True, verbose_name='title', max_length=255)),
                ('og_image', models.ImageField(blank=True, verbose_name='image', upload_to='', storage=libs.storages.media_storage.MediaStorage('seo'))),
                ('og_description', models.TextField(blank=True, verbose_name='description')),
                ('header', models.CharField(blank=True, verbose_name='header', max_length=128)),
                ('text', models.TextField(blank=True, verbose_name='text')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'SEO data',
                'verbose_name_plural': 'SEO data',
            },
        ),
        migrations.AlterUniqueTogether(
            name='seodata',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
