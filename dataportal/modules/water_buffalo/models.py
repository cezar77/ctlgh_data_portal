from django.db import models
from django.contrib.postgres.fields import ArrayField


class Animal(models.Model):
    BREEDS = (
        ('BA', 'Banni'),
        ('BH', 'Bhadawari'),
        ('JA', 'Jaffrabadi/Jaffarabadi'),
        ('MU', 'Murrah'),
        ('PA', 'Pandharpuri'),
        ('SU', 'Surti'),
        ('ME', 'Mediterranean'),
    )
    ENA_BASE_URL = 'https://www.ebi.ac.uk/ena/browser/view/'

    study_accession = models.CharField(max_length=10)
    sample_accession = models.CharField(max_length=12)
    experiment_accession = models.CharField(max_length=10)
    run_accession = models.CharField(max_length=10, unique=True)
    tax_id = models.CharField(max_length=12)
    fastq_ftp = ArrayField(
        models.URLField(max_length=120),
        size=2,
        blank=True,
        verbose_name='FASTQ FTP',
    )
    submitted_ftp = ArrayField(
        models.URLField(max_length=120),
        size=2,
        verbose_name='Submitted FTP',
    )
    sra_ftp = models.URLField(
        max_length=120,
        blank=True,
        verbose_name='SRA FTP'
    )
    breed = models.CharField(
        max_length=2,
        choices=BREEDS,
    )
    species = models.ForeignKey('animals.Species', related_name='water_buffalos')

    def __str__(self):
        return '{} {}'.format(
            self.species.common_name,
            self.sample_accession
        )

    def get_absolute_url(self):
        return reverse('water_buffalo:animal-detail', kwargs={'pk': self.pk})

    def get_study_accession_url(self):
        return '{}{}'.format(self.ENA_BASE_URL, self.study_accession)

    def get_sample_accession_url(self):
        return '{}{}'.format(self.ENA_BASE_URL, self.sample_accession)

    def get_experiment_accession_url(self):
        return '{}{}'.format(self.ENA_BASE_URL, self.experiment_accession)

    def get_run_accession_url(self):
        return '{}{}'.format(self.ENA_BASE_URL, self.run_accession)

    def get_tax_id_url(self):
        return '{}Taxon:{}'.format(self.ENA_BASE_URL, self.tax_id)


