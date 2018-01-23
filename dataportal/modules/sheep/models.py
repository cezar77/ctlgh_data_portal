from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres import fields as pg_fields
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.functional import cached_property
from django.utils.text import slugify


class Population(models.Model):
    TAIL_TYPES = (
        ('FT', 'fat-tailed'),
        ('TT', 'thin-tailed'),
        ('FR', 'fat-rumped'),
    )
    TAIL_SHAPES = (
        ('L', 'long'),
        ('S', 'short'),
    )

    mean_litter_size = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True
    )
    tail_type = models.CharField(
        max_length=2,
        choices=TAIL_TYPES,
        blank=True
    )
    tail_shape = models.CharField(
        max_length=1,
        choices=TAIL_SHAPES,
        blank=True
    )
    further_tail_description = models.CharField(max_length=200, blank=True)
    possible_related_breed = models.CharField(max_length=50)

    def __str__(self):
        return '{} (mean litter size: {})'.format(
            self.possible_related_breed,
            self.mean_litter_size
        )

    @cached_property
    def breed_slug(self):
        return slugify(self.possible_related_breed)


class Sampling(models.Model):
    SITES = (
        ('C', 'communal grazing field'),
        ('V', 'village'),
    )

    date = models.DateField(blank=True, null=True)
    site = models.CharField(max_length=100, choices=SITES, blank=True)
    geolocation = models.PointField(blank=True, null=True)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)
    latitude = models.DecimalField(max_digits=6, decimal_places=4)
    altitude = pg_fields.IntegerRangeField()
    locality = models.CharField(max_length=50, blank=True)
    population = models.OneToOneField('Population', related_name='sampling')

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        related_name='sheep_samplings',
        limit_choices_to={'app_label': 'boundaries'}
    )
    object_id = models.PositiveIntegerField(db_index=True)
    administrative_area = GenericForeignKey('content_type', 'object_id')

    objects = models.GeoManager()

    def __str__(self):
        return 'Sampling from {} for {}'.format(self.date, self.population)

    def save(self, *args, **kwargs):
        self.geolocation = Point(float(self.longitude), float(self.latitude))
        super(Sampling, self).save(*args, **kwargs)

    
class Animal(models.Model):
    SEXES = (
        ('F', 'female'),
        ('M', 'male'),
    )
    animal_id = models.CharField(max_length=10, unique=True)
    animal_sex = models.CharField(
        max_length=1,
        choices=SEXES,
        blank=True
    )
    sampling = models.ForeignKey('Sampling', related_name='animals')
    species = models.ForeignKey('animals.Species', related_name='sheep')

    def __str__(self):
        return '{} {}'.format(
            self.species.common_name,
            self.animal_id
        )
