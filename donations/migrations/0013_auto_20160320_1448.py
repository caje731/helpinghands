# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-20 14:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import donations.models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0012_auto_20160320_0743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.ImageField(max_length=255, upload_to=donations.models.user_dir_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInterviewApproval',
            fields=[
                ('approval_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='donations.Approval')),
                ('case', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='donations.CaseDetail')),
            ],
            bases=('donations.approval',),
        ),
        migrations.CreateModel(
            name='PhoneApproval',
            fields=[
                ('approval_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='donations.Approval')),
                ('case', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='donations.CaseDetail')),
            ],
            bases=('donations.approval',),
        ),
        migrations.CreateModel(
            name='VisitApproval',
            fields=[
                ('approval_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='donations.Approval')),
                ('case', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='donations.CaseDetail')),
            ],
            bases=('donations.approval',),
        ),
        migrations.AddField(
            model_name='approvalattachment',
            name='attached_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donations.Approval'),
        ),
        migrations.AddField(
            model_name='approval',
            name='approver',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='donations.Profile'),
        ),
    ]