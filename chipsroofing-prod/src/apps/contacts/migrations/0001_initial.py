# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('city', models.CharField(verbose_name='city', max_length=255)),
                ('address', models.CharField(verbose_name='address', max_length=255)),
                ('region', models.CharField(verbose_name='region', max_length=64, blank=True)),
                ('zip', models.CharField(verbose_name='zip', max_length=32, blank=True)),
                ('coords', google_maps.fields.GoogleCoordsField(verbose_name='coords', blank=True, help_text='Double click on the map places marker')),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
                'ordering': ('sort_order',),
            },
        ),
        migrations.CreateModel(
            name='ContactBlock',
            fields=[
                ('attachableblock_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='attachable_blocks.AttachableBlock', auto_created=True)),
                ('header', models.CharField(verbose_name='header', max_length=128, blank=True)),
            ],
            options={
                'verbose_name': 'Contact block',
                'verbose_name_plural': 'Contact blocks',
            },
            bases=('attachable_blocks.attachableblock',),
        ),
        migrations.CreateModel(
            name='ContactsConfig',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('header', models.CharField(verbose_name='header', max_length=128)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=128)),
                ('phone', models.CharField(verbose_name='phone', max_length=32, blank=True)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254, blank=True)),
                ('message', models.TextField(verbose_name='message', max_length=2048)),
                ('date', models.DateTimeField(verbose_name='date sent', editable=False, default=django.utils.timezone.now)),
                ('referer', models.CharField(verbose_name='from page', max_length=255, editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
                'default_permissions': ('delete',),
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='NotificationReceiver',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('email', models.EmailField(verbose_name='e-mail', max_length=254)),
                ('config', models.ForeignKey(related_name='receivers', to='contacts.ContactsConfig')),
            ],
            options={
                'verbose_name': 'notification receiver',
                'verbose_name_plural': 'notification receivers',
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('number', models.CharField(verbose_name='number', max_length=255, blank=True)),
                ('sort_order', models.PositiveIntegerField(verbose_name='sort order')),
                ('address', models.ForeignKey(related_name='+', to='contacts.Address')),
            ],
            options={
                'verbose_name': 'phone',
                'verbose_name_plural': 'phones',
                'ordering': ('sort_order',),
            },
        ),
    ]
