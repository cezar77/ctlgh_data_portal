# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-10-01 15:33
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('animals', '0002_species_app'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_accession', models.CharField(max_length=10)),
                ('sample_accession', models.CharField(max_length=12)),
                ('experiment_accession', models.CharField(max_length=10)),
                ('run_accession', models.CharField(max_length=10)),
                ('tax_id', models.CharField(max_length=12)),
                ('fastq_ftp', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=120), size=2)),
                ('submitted_ftp', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=120), size=2)),
                ('sra_ftp', models.URLField(max_length=120)),
                ('breed', models.CharField(choices=[('BA', 'Banni'), ('BH', 'Bhadawari'), ('JA', 'Jaffrabadi/Jaffarabadi'), ('MU', 'Murrah'), ('PA', 'Pandharpuri'), ('SU', 'Surti'), ('ME', 'Mediterranean')], max_length=2)),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='water_buffalos', to='animals.Species')),
            ],
        ),
    ]