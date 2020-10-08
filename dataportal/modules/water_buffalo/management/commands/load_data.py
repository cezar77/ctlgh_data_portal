import argparse
import json
import re

from django.core.management.base import BaseCommand

from dataportal.modules.animals.models import Species
from dataportal.modules.water_buffalo.models import Animal


class Command(BaseCommand):
    help = "Load data for water buffalo"

    breeds = {
       'BA': r'B[au]nni',
       'BH': r'Bhad[ah]wari',
       'JA': r'Jaffa?rabadi',
       'MU': r'Murrah',
       'PA': r'Padharpuri',
       'SU': r'Surti',
       'ME': r'Mediterranean', 
    }

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            type=argparse.FileType('r'),
            help='JSON file with data for water buffalo'
        )

    def handle(self, *args, **options):
        filename = options['filename']
        samples = json.load(filename)
        result = list(map(self.process_samples, samples))
        print(result)

    def process_samples(self, sample):
        sample_accession = sample.get('sample_accession')
        fastq_ftp = self.get_urls(sample.get('fastq_ftp'))
        submitted_ftp = self.get_urls(sample.get('submitted_ftp'))
        breed = self.get_breed(sample.get('submitted_ftp'))
        breed = '' if breed == [] else breed[0][0]
        species = Species.objects.get(slug='bubalus-bubalis')
        record = {
            'study_accession': sample.get('study_accession'),
            'sample_accession': sample_accession,
            'experiment_accession': sample.get('experiment_accession'),
            'run_accession': sample.get('run_accession'),
            'tax_id': sample.get('tax_id'),
            'fastq_ftp': fastq_ftp,
            'submitted_ftp': submitted_ftp,
            'sra_ftp': sample.get('sra_ftp'),
            'breed': breed,
            'species': species,
        }
        Animal.objects.update_or_create(
            sample_accession=sample_accession,
            defaults=record
        )

    def get_urls(self, entry):
        return entry.split(';')

    def get_breed(self, filename):
        result = list(filter(lambda b: re.search(b[1], filename), self.breeds.items()))
        return result

