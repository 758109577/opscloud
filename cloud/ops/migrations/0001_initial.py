# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 04:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('passwd', models.CharField(max_length=30)),
                ('deptment', models.CharField(max_length=30)),
            ],
        ),
    ]