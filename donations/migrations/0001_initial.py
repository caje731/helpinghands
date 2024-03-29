# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 21:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import donations.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_name', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('pincode', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acc_holder_name', models.CharField(max_length=255, verbose_name="Account Holder's Name")),
                ('acc_number', models.CharField(max_length=255, verbose_name='Account Number')),
                ('bank_name', models.CharField(max_length=255)),
                ('branch_name', models.CharField(max_length=255)),
                ('ifsc', models.CharField(max_length=11, verbose_name='IFSC')),
                ('cheque_copy', models.ImageField(max_length=255, upload_to=donations.models.user_dir_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CaseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.PositiveSmallIntegerField(choices=[(1, 'Medical/Health'), (2, 'Education'), (3, 'Support due to loss of parent(s)'), (4, 'Other (please mention the reason)')], default=1)),
                ('reason_phrase', models.CharField(blank=True, max_length=255)),
                ('brief', models.CharField(max_length=255, verbose_name='Brief of the case')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Registered'), (2, 'Under Verification'), (3, 'Verified'), (4, 'Rejected'), (5, 'Closed')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_donor', models.BooleanField()),
                ('cell_phone', models.CharField(max_length=255)),
                ('res_phone', models.CharField(max_length=255, null=True, verbose_name='Residence Phone')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.Address')),
                ('bank_details', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.BankDetail')),
                ('case_details', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.CaseDetail')),
            ],
        ),
        migrations.CreateModel(
            name='Referrer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255, verbose_name='Office Phone')),
                ('email', models.EmailField(max_length=254, verbose_name='Office Email')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='referrer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.Referrer'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='work',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.WorkDetail'),
        ),
    ]
