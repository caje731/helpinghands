# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-18 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0021_auto_20180218_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casedetail',
            name='postclosure_gallery',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postclosure_casedetail', to='photologue.Gallery'),
        ),
        migrations.AlterField(
            model_name='casedetail',
            name='preclosure_gallery',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preclosure_casedetail', to='photologue.Gallery'),
        ),
    ]
