# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-10 11:35
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chickens', '0004_auto_20180110_0905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='farm',
            old_name='previous_illnes_occurence',
            new_name='previous_illness_occurence',
        ),
        migrations.AddField(
            model_name='farm',
            name='altitude',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='farm',
            name='geolocation',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
