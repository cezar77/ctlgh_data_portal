# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-10-02 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0002_species_app'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='ncbi_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='NCBI ID'),
        ),
    ]