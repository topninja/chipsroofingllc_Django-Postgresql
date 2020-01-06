# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0004_auto_20170908_0723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regularcampaign',
            name='status',
        ),
        migrations.RemoveField(
            model_name='regularcampaign',
            name='published',
        ),
        migrations.RemoveField(
            model_name='regularcampaign',
            name='remote_mail_id',
        ),
        migrations.RemoveField(
            model_name='regularcampaign',
            name='sent',
        ),
        migrations.AddField(
            model_name='group',
            name='created',
            field=models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='group',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='modified'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='regularcampaign',
            name='created',
            field=models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='regularcampaign',
            name='export_allowed',
            field=models.BooleanField(default=False, verbose_name='export allowed'),
        ),
        migrations.AddField(
            model_name='regularcampaign',
            name='status',
            field=models.CharField(max_length=16, verbose_name='status',
                choices=[('draft', 'Draft'), ('outbox', 'Outbox'), ('sent', 'Sent')], default='draft'),
        ),
        migrations.AddField(
            model_name='regularcampaign',
            name='from_email',
            field=models.EmailField(verbose_name='sender e-mail', max_length=254, blank=True),
        ),
        migrations.AddField(
            model_name='regularcampaign',
            name='from_name',
            field=models.CharField(verbose_name='sender name', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='regularcampaign',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='modified'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='regularcampaign',
            name='total_recipients',
            field=models.PositiveIntegerField(editable=False, default=0, verbose_name='total recipients'),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='created',
            field=models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='modified'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mailerconfig',
            name='from_email',
            field=models.EmailField(help_text='must be valid and actually exists', default='manager@example.com', verbose_name='sender e-mail', max_length=254),
        ),
        migrations.AlterField(
            model_name='mailerconfig',
            name='from_name',
            field=models.CharField(help_text='should be your name', default='John Smith', verbose_name='sender name', max_length=255),
        ),
        migrations.AlterField(
            model_name='regularcampaign',
            name='clicked',
            field=models.PositiveIntegerField(editable=False, default=0, verbose_name='clicked'),
        ),
        migrations.AlterField(
            model_name='regularcampaign',
            name='groups',
            field=models.ManyToManyField(verbose_name='recipients', to='mailerlite.Group'),
        ),
        migrations.AlterField(
            model_name='regularcampaign',
            name='opened',
            field=models.PositiveIntegerField(editable=False, default=0, verbose_name='opened'),
        ),
        migrations.AlterField(
            model_name='regularcampaign',
            name='remote_id',
            field=models.BigIntegerField(db_index=True, default=0, verbose_name='ID in Mailerlite'),
        ),
    ]
