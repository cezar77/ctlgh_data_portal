# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-10-02 08:06
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water_buffalo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='breed',
            field=models.CharField(choices=[('BA', 'Banni'), ('BH', 'Bhada?wari'), ('JA', 'Jaffrabadi/Jaffarabadi'), ('MU', 'Murrah'), ('PA', 'Pandharpuri'), ('SU', 'Surti'), ('ME', 'Mediterranean')], max_length=2),
        ),
        migrations.AlterField(
            model_name='animal',
            name='fastq_ftp',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=120), blank=True, size=2),
        ),
        migrations.AlterField(
            model_name='animal',
            name='sample_accession',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='animal',
            name='sra_ftp',
            field=models.URLField(blank=True, max_length=120),
        ),
    ]
