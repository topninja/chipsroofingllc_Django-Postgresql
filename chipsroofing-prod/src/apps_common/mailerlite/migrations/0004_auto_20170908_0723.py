# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailerlite', '0003_auto_20170905_0746'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='campaign',
            new_name='regularcampaign',
        )
    ]
