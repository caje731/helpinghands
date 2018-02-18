# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-18 12:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0010_auto_20160105_1307'),
        ('donations', '0020_auto_20160606_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='casedetail',
            name='postclosure_gallery',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='postclosure_casedetail', to='photologue.Gallery'),
        ),
        migrations.AddField(
            model_name='casedetail',
            name='preclosure_gallery',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='preclosure_casedetail', to='photologue.Gallery'),
        ),
    ]
