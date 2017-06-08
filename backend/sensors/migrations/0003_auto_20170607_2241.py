# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-07 22:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0002_auto_20170606_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='host_key',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='measurementvalue',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]