# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-11 11:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_url', models.URLField(max_length=255, unique=True)),
                ('file_url', models.URLField(max_length=255, unique=True)),
                ('attribution', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('slug', models.SlugField()),
                ('species', models.CharField(max_length=30)),
                ('genus', models.CharField(max_length=30)),
                ('subfamily', models.CharField(blank=True, max_length=30)),
                ('family', models.CharField(max_length=30)),
                ('order', models.CharField(max_length=30)),
                ('class_name', models.CharField(db_column='class', max_length=30, verbose_name='class')),
                ('phylum', models.CharField(max_length=30)),
                ('ncbi_id', models.PositiveSmallIntegerField(unique=True, verbose_name='NCBI ID')),
                ('image', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='species', to='animals.Image')),
            ],
            options={
                'verbose_name': 'Species',
                'ordering': ('genus', 'species'),
                'verbose_name_plural': 'Species',
            },
        ),
    ]