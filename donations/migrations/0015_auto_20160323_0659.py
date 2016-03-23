# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-23 06:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import donations.models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0014_auto_20160320_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalattachment',
            name='attached_for',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='donations.Approval'),
        ),
        migrations.AlterField(
            model_name='approvalattachment',
            name='attachment',
            field=models.ImageField(max_length=255, upload_to=donations.models.approvalattachment_upload_path),
        ),
    ]
