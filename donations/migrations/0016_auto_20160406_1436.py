# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-06 14:36
from __future__ import unicode_literals

from django.db import migrations, models
import donations.models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0015_auto_20160323_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='casedetail',
            name='approved_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='bankdetail',
            name='cheque_copy',
            field=models.ImageField(max_length=255, upload_to=donations.models.cheque_copy_upload_path),
        ),
        migrations.AlterField(
            model_name='casedetail',
            name='reason',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Medical'), (2, 'Basic Education')], default=1),
        ),
    ]