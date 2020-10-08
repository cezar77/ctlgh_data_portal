# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-08 11:44
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water_buffalo', '0002_auto_20201002_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='breed',
            field=models.CharField(choices=[('BA', 'Banni'), ('BH', 'Bhadawari'), ('JA', 'Jaffrabadi/Jaffarabadi'), ('MU', 'Murrah'), ('PA', 'Pandharpuri'), ('SU', 'Surti'), ('ME', 'Mediterranean')], max_length=2),
        ),
        migrations.AlterField(
            model_name='animal',
            name='fastq_ftp',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=120), blank=True, size=2, verbose_name='FASTQ FTP'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='run_accession',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='animal',
            name='sample_accession',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='animal',
            name='sra_ftp',
            field=models.URLField(blank=True, max_length=120, verbose_name='SRA FTP'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='submitted_ftp',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=120), size=2, verbose_name='Submitted FTP'),
        ),
    ]
