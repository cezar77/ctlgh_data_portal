# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-29 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chickens', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='altitude',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
