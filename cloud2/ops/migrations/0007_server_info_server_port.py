# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0006_auto_20170802_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='server_info',
            name='server_port',
            field=models.IntegerField(null=True),
        ),
    ]