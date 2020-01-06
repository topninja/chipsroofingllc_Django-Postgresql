# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_networks', '0002_sociallinks_social_instagram'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('google_apikey', models.CharField(verbose_name='API Key', blank=True, max_length=48, default='AIzaSyB4CphiSoXhku-rP9m5-QkXE9U11OJkOzg')),
                ('twitter_app_id', models.CharField(verbose_name='API Key', blank=True, max_length=48)),
                ('twitter_secret', models.CharField(verbose_name='API Secret', blank=True, max_length=64)),
                ('twitter_access_token', models.CharField(verbose_name='Access Token', blank=True, max_length=64)),
                ('twitter_access_token_secret', models.CharField(verbose_name='Access Token Secret', blank=True, max_length=64)),
                ('facebook_access_token', models.TextField(blank=True, verbose_name='Access Token')),
                ('linkedin_access_token', models.TextField(blank=True, verbose_name='Access Token')),
                ('instagram_client_id', models.CharField(verbose_name='Client Key', blank=True, max_length=48)),
                ('instagram_client_secret', models.CharField(verbose_name='Client Secret', blank=True, max_length=48)),
                ('instagram_redirect_uri', models.URLField(verbose_name='Redirect URI', blank=True)),
                ('instagram_access_token', models.CharField(verbose_name='Access Token', blank=True, max_length=64)),
                ('updated', models.DateTimeField(verbose_name='change date', auto_now=True)),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Settings',
            },
        ),
    ]
