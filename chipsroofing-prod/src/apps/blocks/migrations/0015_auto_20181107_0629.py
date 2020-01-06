# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import libs.storages.media_storage
import ckeditor.fields
import libs.videolink_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0005_auto_20180828_0145'),
        ('blocks', '0014_auto_20181004_0624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=255)),
                ('video', libs.videolink_field.fields.VideoLinkField(verbose_name='video', providers=set(['youtube']), blank=True)),
                ('video_webm', models.FileField(verbose_name='video WebM', storage=libs.storages.media_storage.MediaStorage('main/video'), upload_to='', blank=True)),
                ('video_mp4', models.FileField(verbose_name='video MP4', storage=libs.storages.media_storage.MediaStorage('main/video'), upload_to='', blank=True)),
                ('content', ckeditor.fields.CKEditorUploadField(verbose_name='video and content', help_text='Image sizes: from <b>800x450</b> to <b>1024x576</b>', blank=True)),
                ('sort_order', models.IntegerField(verbose_name='order', default=0)),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'videos',
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='VideosBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to='attachable_blocks.AttachableBlock')),
                ('video_title', models.CharField(verbose_name='header', max_length=255)),
            ],
            options={
                'verbose_name': 'Videos',
                'verbose_name_plural': 'Videos',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.AddField(
            model_name='video',
            name='config',
            field=models.OneToOneField(related_name='videos', to='blocks.VideosBlock'),
        ),
    ]
