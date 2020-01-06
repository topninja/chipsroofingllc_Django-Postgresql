# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachableblock',
            old_name='block_content_type',
            new_name='content_type',
        ),
        migrations.AlterField(
            model_name='attachablereference',
            name='content_type',
            field=models.ForeignKey(related_name='+', help_text='content type of entity, attached to', to='contenttypes.ContentType'),
        ),
    ]
