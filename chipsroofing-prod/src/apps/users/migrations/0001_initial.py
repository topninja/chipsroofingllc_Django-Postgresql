# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import libs.stdimage.fields
import django.contrib.auth.models
import django.utils.timezone
import libs.storages.media_storage


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(unique=True, max_length=30, error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', libs.stdimage.fields.StdImageField(blank=True, min_dimensions=(150, 150), storage=libs.storages.media_storage.MediaStorage('users/avatar'), aspects='normal', variations={'small': {'size': (50, 50)}, 'micro': {'size': (32, 32)}, 'normal': {'size': (150, 150)}}, verbose_name='avatar', upload_to='')),
                ('avatar_crop', models.CharField(blank=True, verbose_name='stored_crop', editable=False, max_length=32)),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group', related_query_name='user', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(blank=True, to='auth.Permission', related_query_name='user', verbose_name='user permissions', help_text='Specific permissions for this user.', related_name='user_set')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'permissions': (('admin_menu', 'Can see hidden menu items'),),
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
