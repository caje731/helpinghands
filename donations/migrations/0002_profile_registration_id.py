# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-01 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='registration_id',
            field=models.CharField(default=b'2016-01-01 03:35:09.859032+00:00', max_length=255, unique=True, verbose_name='Registration ID'),
            preserve_default=False,
        ),
    ]
