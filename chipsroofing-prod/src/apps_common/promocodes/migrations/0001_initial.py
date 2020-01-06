# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django.utils.timezone
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=128)),
                ('code', models.CharField(validators=[django.core.validators.MinLengthValidator(4)], max_length=24, unique=True, verbose_name='code')),
                ('strategy_name', models.CharField(choices=[('fixed_amount', 'Fixed monetary amount'), ('percent', 'Percentage discount')], verbose_name='action', max_length=64)),
                ('parameter', models.CharField(default='0', blank=True, max_length=32, verbose_name='parameter')),
                ('redemption_limit', models.PositiveIntegerField(default=1, help_text='zero sets the limit to unlimited', verbose_name='redemption limit')),
                ('start_date', models.DateTimeField(verbose_name='start time', null=True, blank=True)),
                ('end_date', models.DateTimeField(verbose_name='end time', null=True, blank=True)),
                ('self_created', models.BooleanField(default=False, verbose_name='self-created')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created on')),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'verbose_name': 'promo code',
                'ordering': ('-created',),
                'verbose_name_plural': 'promo codes',
            },
        ),
        migrations.CreateModel(
            name='PromoCodeReference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('applied', models.BooleanField(default=False, editable=False, verbose_name='applied')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created on')),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
                ('promocode', models.ForeignKey(related_name='references', verbose_name='promo code', to='promocodes.PromoCode')),
            ],
            options={
                'verbose_name': 'promo code reference',
                'ordering': ('-created',),
                'verbose_name_plural': 'promo code references',
            },
        ),
        migrations.CreateModel(
            name='PromoSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('subscribe_note', models.CharField(verbose_name='subscribe header', blank=True, max_length=128)),
                ('subscribe_strategy_name', models.CharField(choices=[('fixed_amount', 'Fixed monetary amount'), ('percent', 'Percentage discount')], verbose_name='action', max_length=64)),
                ('subscribe_parameter', models.CharField(default='0', blank=True, max_length=32, verbose_name='parameter')),
                ('subscribe_email', ckeditor.fields.CKEditorUploadField(verbose_name='email template')),
            ],
            options={
                'verbose_name': 'settings',
                'default_permissions': ('change',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='promocodereference',
            unique_together=set([('promocode', 'content_type', 'object_id')]),
        ),
    ]
