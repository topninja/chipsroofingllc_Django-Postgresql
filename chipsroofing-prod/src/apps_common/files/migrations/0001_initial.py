# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import libs.file_field.fields
import files.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('file', libs.file_field.fields.FileField(storage=libs.storages.media_storage.MediaStorage('files'), max_length=150, verbose_name='file')),
                ('name', models.CharField(help_text='If you leave it empty the file name will be used', max_length=150, verbose_name='name', blank=True)),
                ('set_name', models.CharField(max_length=32, default='default', verbose_name='set name')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', related_name='+')),
            ],
            options={
                'verbose_name': 'file',
                'ordering': ('sort_order',),
                'verbose_name_plural': 'files',
            },
        ),
        migrations.AlterIndexTogether(
            name='pagefile',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
    ]
