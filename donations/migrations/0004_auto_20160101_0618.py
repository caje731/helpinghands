# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-01 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_auto_20160101_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cell_phone',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
