# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-03 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20171103_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
