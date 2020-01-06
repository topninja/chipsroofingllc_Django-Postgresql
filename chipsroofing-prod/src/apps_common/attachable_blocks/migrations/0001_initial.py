# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachableBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('label', models.CharField(verbose_name='label', help_text='For inner use', max_length=128)),
                ('visible', models.BooleanField(default=True, verbose_name='visible')),
                ('created', models.DateTimeField(verbose_name='create date', editable=False)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='change date')),
                ('block_content_type', models.ForeignKey(to='contenttypes.ContentType', null=True, editable=False, related_name='+')),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'attachable block',
                'ordering': ('label',),
                'verbose_name_plural': 'attachable blocks',
            },
        ),
        migrations.CreateModel(
            name='AttachableReference',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('ajax', models.BooleanField(default=False, verbose_name='AJAX', help_text='load block through AJAX')),
                ('set_name', models.CharField(default='default', verbose_name='set name', max_length=32)),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='sort order')),
                ('block', models.ForeignKey(to='attachable_blocks.AttachableBlock', verbose_name='block', related_name='references')),
                ('block_ct', models.ForeignKey(to='contenttypes.ContentType', null=True, related_name='+')),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'attached block',
                'ordering': ('set_name', 'sort_order'),
                'verbose_name_plural': 'attached blocks',
            },
        ),
        migrations.AlterIndexTogether(
            name='attachablereference',
            index_together=set([('content_type', 'object_id', 'set_name')]),
        ),
    ]
