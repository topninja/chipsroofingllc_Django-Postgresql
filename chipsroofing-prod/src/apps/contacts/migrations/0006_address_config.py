# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20180910_0604'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='config',
            field=models.OneToOneField(default=1243542, to='contacts.ContactsConfig', related_name='address'),
            preserve_default=False,
        ),
    ]
