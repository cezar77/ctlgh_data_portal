# -*- coding: utf-8 -*-
import os
import zipfile
import re
import argparse

import wget

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.gis.utils import LayerMapping

from dataportal.modules.boundaries.models import (
    Country,
    FirstAdministrativeLevel,
    SecondAdministrativeLevel,
    ThirdAdministrativeLevel,
    FourthAdministrativeLevel,
    FifthAdministrativeLevel
)
from dataportal.modules.boundaries.mappings import (
    country_mapping,
    adm1_mapping,
    adm2_mapping,
    adm3_mapping,
    adm4_mapping,
    adm5_mapping
)


def country_iso_code(string):
    value = string.upper()
    if not re.match('[A-Z]{3}$', value):
        raise argparse.ArgumentError()
    return value
        

class Command(BaseCommand):
    help = "Download country shapefiles, unzip them and populate the database."

    models = (
        Country,
        FirstAdministrativeLevel,
        SecondAdministrativeLevel,
        ThirdAdministrativeLevel,
        FourthAdministrativeLevel,
        FifthAdministrativeLevel
    )
    mappings = (
        country_mapping,
        adm1_mapping,
        adm2_mapping,
        adm3_mapping,
        adm4_mapping,
        adm5_mapping
    )

    base_url = 'http://biogeo.ucdavis.edu/data/gadm2.8/shp/'
    zipfile_name = '{iso}_adm_shp.zip'
    dir_path = settings.BASE_DIR

    def add_arguments(self, parser):
        parser.add_argument(
            'country_code',
            type=country_iso_code,
            help='3-letter ISO country code',
        )
        parser.add_argument(
            '--levels',
            type=int,
            choices=range(7),
            default=0,
            help='Number of administrative levels',
        )

    def handle(self, *args, **options):
        country_code = options['country_code']
        levels = options['levels']
        self.stdout.write(
            self.style.SUCCESS(
                """
    The DB will be populated with data for {}. If needed the
    correspondent zip file will be downloaded from internet.
------------------------------------------------------------------------
                """.format(country_code)
            )
        )
        self.check_db_entry_exists(country_code)
        if self.create_directory(country_code):
            self.download_file(country_code)
        else:
            if not self.check_unzipped_files_exist(country_code, levels):
                if self.check_ziparchive_exists(country_code):
                    self.unzip_file(country_code)
                else:
                    self.download_file(country_code)
        self.populate_database(country_code)
        
    def check_db_entry_exists(self, country_code):
        if Country.objects.filter(iso=country_code).exists():
            raise CommandError(
                ('A DB entry for {} already exists.'
                 'Please consult the DB admin.').format(
                    country_code
                )
            )
        self.stdout.write(
            self.style.SUCCESS(
                ('There is no DB entry for {}.'
                 'The database will be populated.').format(
                    country_code
                )
            )
        )

    def create_directory(self, country_code):
        self.dir_path = os.path.join(settings.BASE_DIR, 'data', country_code)
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
            self.stdout.write(
                self.style.SUCCESS(
                    'The directory {} was created.'.format(self.dir_path)
                )
            )
            return True
        self.stdout.write(
            self.style.SUCCESS(
                'The directory {} already exists.'.format(self.dir_path)
            )
        )
        return False
            
    def check_unzipped_files_exist(self, country_code, levels):
        file_extensions = ['cpg', 'csv', 'dbf', 'prj', 'shp', 'shx']
        filename = '{}_adm{}.{}'
        for i in range(levels):
            for extension in file_extensions:
                if not os.path.exists(
                    os.path.join(
                        self.dir_path,
                        filename.format(country_code, i, extension)
                    )
                ):
                    self.stdout.write(
                        self.style.SUCCESS(
                            "At least one of the needed files doesn't exist."
                        )
                    )
                    return False
        self.stdout.write(
            self.style.NOTICE(
                "All needed files are present."
            )
        )
        return True
        
    def check_ziparchive_exists(self, country_code):
        return os.path.exists(
            os.path.join(
                self.dir_path,
                self.zipfile_name.format(iso=country_code)
            )
        )

    def download_file(self, country_code):
        file_name = self.zipfile_name.format(iso=country_code)
        download_url = self.base_url + file_name
        print(download_url)
        try:
            downloaded_file = wget.download(
                download_url,
                out=self.dir_path
            )
            self.stdout.write('\nZIP file downloaded.')
            self.unzip_file(country_code)
        except:
            raise CommandError(
                'File {} could not be downloaded!'.format(file_name)
            )

    def unzip_file(self, country_code):
        zip_file = os.path.join(
            self.dir_path,
            self.zipfile_name.format(iso=country_code)
        )
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(self.dir_path)

    def populate_database(self, country_code):
        filename = '{iso}_adm{level}.shp'
        for i in range(6):
            shp = os.path.join(
                self.dir_path,
                filename.format(iso=country_code, level=i))
            if os.path.exists(shp):
                lm = LayerMapping(
                    self.models[i], shp, self.mappings[i],
                    transform=False, encoding='utf-8',
                )
                lm.save(strict=True, verbose=True)
