# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 04:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0004_node_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='permission',
            field=models.IntegerField(max_length=11, null=True),
        ),
    ]
