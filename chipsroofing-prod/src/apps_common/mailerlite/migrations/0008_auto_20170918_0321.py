# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0007_auto_20170916_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='need_export',
            field=models.BooleanField(verbose_name='need export', default=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='date_created',
            field=models.DateTimeField(verbose_name='date created', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='date_updated',
            field=models.DateTimeField(verbose_name='date updated', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='regularcampaign',
            name='date_created',
            field=models.DateTimeField(verbose_name='date created', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='date_created',
            field=models.DateTimeField(verbose_name='date subscribed', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='date_subscribe',
            field=models.DateTimeField(verbose_name='date subscribe', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='date_updated',
            field=models.DateTimeField(verbose_name='date updated', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='groups',
            field=models.ManyToManyField(verbose_name='groups', to='mailerlite.Group'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='remote_id',
            field=models.BigIntegerField(db_index=True, verbose_name='ID in Mailerlite', default=0),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='status',
            field=models.CharField(verbose_name='status', default='active', max_length=32, choices=[('active', 'Active'), ('unconfirmed', 'Unconfirmed'), ('unsubscribed', 'Unsubscribed'), ('bounced', 'Bounced'), ('junk', 'Junk')]),
        ),
    ]
