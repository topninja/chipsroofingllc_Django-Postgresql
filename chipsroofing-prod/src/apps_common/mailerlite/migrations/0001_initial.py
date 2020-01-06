# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import libs.storages.media_storage
import django.utils.timezone
import libs.color_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('text', ckeditor.fields.CKEditorUploadField(verbose_name='text')),
                ('sent', models.PositiveIntegerField(default=0, editable=False, verbose_name='sent emails')),
                ('opened', models.PositiveIntegerField(default=0, editable=False, verbose_name='opened emails')),
                ('clicked', models.PositiveIntegerField(default=0, editable=False, verbose_name='clicks from emails')),
                ('status', models.SmallIntegerField(default=0, choices=[(0, 'Draft'), (10, 'Queued'), (20, 'Running'), (30, 'Done')], verbose_name='status')),
                ('published', models.BooleanField(default=False, verbose_name='published')),
                ('remote_id', models.BigIntegerField(default=0, editable=False, db_index=True, verbose_name='ID in Mailerlite')),
                ('remote_mail_id', models.BigIntegerField(default=0, editable=False, db_index=True, verbose_name='ID in Mailerlite')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='date created')),
                ('date_started', models.DateTimeField(editable=False, null=True, verbose_name='date started')),
                ('date_done', models.DateTimeField(editable=False, null=True, verbose_name='date done')),
            ],
            options={
                'verbose_name_plural': 'campaigns',
                'ordering': ('-date_created',),
                'verbose_name': 'campaign',
                'default_permissions': ('add', 'change'),
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('subscribable', models.BooleanField(default=False, verbose_name='subscribable')),
                ('total', models.PositiveIntegerField(default=0, editable=False, verbose_name='total subscribers')),
                ('active', models.PositiveIntegerField(default=0, editable=False, verbose_name='active subscribers')),
                ('unsubscribed', models.PositiveIntegerField(default=0, editable=False, verbose_name='unsubscribed')),
                ('status', models.SmallIntegerField(default=0, choices=[(0, 'Queued'), (10, 'Published')], verbose_name='status')),
                ('sent', models.PositiveIntegerField(default=0, editable=False, verbose_name='sent emails')),
                ('opened', models.PositiveIntegerField(default=0, editable=False, verbose_name='opened emails')),
                ('clicked', models.PositiveIntegerField(default=0, editable=False, verbose_name='clicks from emails')),
                ('remote_id', models.BigIntegerField(default=0, editable=False, db_index=True, verbose_name='ID in Mailerlite')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
            options={
                'verbose_name_plural': 'lists',
                'ordering': ('-date_created',),
                'verbose_name': 'list',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='MailerConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('from_email', models.EmailField(max_length=254, help_text='must be valid and actually exists', default='manager@example.com', verbose_name='e-mail')),
                ('from_name', models.CharField(max_length=255, help_text='should be your name', default='John Smith', verbose_name='name')),
                ('bg_color', libs.color_field.fields.ColorField(blank=True, default='#BDC3C7', verbose_name='background color')),
                ('bg_image', models.ImageField(storage=libs.storages.media_storage.MediaStorage('mailerlite/campaigns'), blank=True, upload_to='', verbose_name='background image')),
                ('footer_text', models.TextField(blank=True, verbose_name='text')),
                ('website', models.URLField(max_length=255, verbose_name='website address')),
                ('contact_email', models.EmailField(max_length=254, default='admin@example.com', verbose_name='contact email')),
                ('import_groups_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('import_campaigns_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('import_subscribers_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('export_groups_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('export_campaigns_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('export_subscribers_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('name', models.CharField(max_length=255, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=255, blank=True, verbose_name='last name')),
                ('company', models.CharField(max_length=255, blank=True, verbose_name='company')),
                ('status', models.SmallIntegerField(default=0, choices=[(0, 'Queued'), (10, 'Subscribed'), (-10, 'Unsubscribed'), (-20, 'Not exists')], verbose_name='status')),
                ('sent', models.PositiveIntegerField(default=0, editable=False, verbose_name='sent emails')),
                ('opened', models.PositiveIntegerField(default=0, editable=False, verbose_name='opened emails')),
                ('clicked', models.PositiveIntegerField(default=0, editable=False, verbose_name='clicks from emails')),
                ('remote_id', models.BigIntegerField(default=0, editable=False, db_index=True, verbose_name='ID in Mailerlite')),
                ('date_created', models.DateField(default=django.utils.timezone.now, editable=False, verbose_name='date subscribed')),
                ('date_unsubscribe', models.DateTimeField(editable=False, null=True, verbose_name='date unsubscribed')),
                ('groups', models.ManyToManyField(to='mailerlite.Group')),
            ],
            options={
                'verbose_name_plural': 'subscribers',
                'ordering': ('-date_created', 'id'),
                'verbose_name': 'subscriber',
                'default_permissions': ('add', 'change'),
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='groups',
            field=models.ManyToManyField(to='mailerlite.Group', verbose_name='lists'),
        ),
    ]
