# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180911_0831'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='header', blank=True)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='order')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
            },
        ),
        migrations.AddField(
            model_name='testimonialspageconfig',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='testimonialspageconfig',
            name='title',
            field=models.CharField(max_length=128, verbose_name='header', blank=True),
        ),
        migrations.AddField(
            model_name='testimonials',
            name='config',
            field=models.ForeignKey(related_name='testimonials', to='main.TestimonialsPageConfig', default=True),
        ),
    ]
