# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedPost',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('network', models.CharField(default='facebook', verbose_name='social network', max_length=32, choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('google', 'Google Plus'), ('linkedin', 'Linked In')])),
                ('text', models.TextField(verbose_name='text')),
                ('url', models.URLField(verbose_name='URL')),
                ('scheduled', models.BooleanField(default=True, verbose_name='sheduled to share')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True, editable=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created on', editable=False)),
                ('posted', models.DateTimeField(null=True, verbose_name='posted on', editable=False)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True, editable=False)),
            ],
            options={
                'verbose_name': 'feed post',
                'ordering': ('-scheduled', '-created'),
                'verbose_name_plural': 'feeds',
            },
        ),
        migrations.CreateModel(
            name='SocialLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('social_facebook', models.URLField(blank=True, verbose_name='facebook', max_length=255)),
                ('social_twitter', models.URLField(blank=True, verbose_name='twitter', max_length=255)),
                ('social_google', models.URLField(blank=True, verbose_name='google plus', max_length=255)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Links',
            },
        ),
        migrations.AlterIndexTogether(
            name='feedpost',
            index_together=set([('network', 'content_type', 'object_id')]),
        ),
    ]
