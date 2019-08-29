import json

from django.core.management.base import BaseCommand, CommandError

from ...models import Animal


class Command(BaseCommand):
    help = (
        'Run through all animals (sheep) and find the associated SRA object.'
        'Update the database with the sample name and the accession url.'
    )

    def handle(self, *args, **options):
        sra_objects = self.filter_sra_objects()
        for obj in sra_objects:
            sheep = Animal.objects.filter(animal_id=obj['sample_title']).update(
                sample_name=obj['sample_name'],
                accession_url=obj['url']
            )

    @staticmethod
    def filter_sra_objects():
        with open('dataportal/modules/sheep/data/sra.json') as jsonfile:
            data = json.load(jsonfile)
        animals = Animal.objects.all()
        sra_objects = []
        for animal in animals:
            sra_objects.extend([item for item in data if item['sample_title'] == animal.animal_id])
        return sra_objects 
