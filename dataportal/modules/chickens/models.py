from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres import fields as pg_fields
from django.utils.functional import cached_property
from django.urls import reverse


class Farm(models.Model):
    SOIL_TYPES = (
        ('VS', 'Vertisol'),
        ('SC', 'Sandy and clay'),
        ('SA', 'Sandy'),
    )
    VEGETATION_TYPES = (
        ('FO', 'Forest'),
        ('SH', 'Shrub'),
        ('RL', 'Range land/grass'),
        ('BL', 'Bare land'),
    )
    RAINFALL_PATTERNS = (
        ('U', 'Unimodal'),
        ('B', 'Bimodal'),
    )
    WATER_SOURCES = (
        ('WE', 'Well',),
        ('TW', 'Tap water'),
        ('RI', 'River'),
        ('SW', 'Spring water'),
        ('DW', 'Deep well pump water'),
    )

    latitude = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        null=True,
        blank=True
    )
    altitude = models.PositiveSmallIntegerField(null=True, blank=True)
    geolocation = models.PointField(null=True, blank=True)
    village = models.CharField(max_length=50, blank=True)
    soil_type = models.CharField(
        max_length=2,
        choices=SOIL_TYPES,
        blank=True
    )
    vegetation_type = models.CharField(
        max_length=2,
        choices=VEGETATION_TYPES,
        blank=True
    )
    agroecology = models.CharField(max_length=100, blank=True)
    rainfall_pattern = models.CharField(
        max_length=1,
        choices=RAINFALL_PATTERNS,
        blank=True
    )
    water_source = models.CharField(
        max_length=2,
        choices=WATER_SOURCES,
        blank=True
    )
    coop_type = models.CharField(max_length=100, blank=True)
    previous_illness_occurence = models.CharField(max_length=100, blank=True)
    chicken_feed = pg_fields.JSONField(null=True, blank=True)
    other_animals = pg_fields.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.geolocation = Point(float(self.longitude), float(self.latitude))
        super(Farm, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('farm-detail', kwargs={'pk': str(self.pk)})


class Animal(models.Model):
    SEXES = (
        ('F', 'female'),
        ('M', 'male'),
    )
    ORIGINS = (
        ('FG', 'Farmgate'),
        ('MA', 'Market'),
        ('NE', 'Neighbour'),
        ('ES', 'Extension service input delivery'),
        ('NG', 'NGO'),
    )

    animal_id = models.CharField(max_length=20)
    tag = models.CharField('tag number or color', max_length=30, blank=True)
    animal_sex = models.CharField(
        max_length=1,
        choices=SEXES,
        blank=True
    )
    origin = models.CharField(
        max_length=2,
        choices=ORIGINS,
        blank=True
    )
    phenotypical_characteristics = pg_fields.JSONField(null=True, blank=True)
    vaccination = models.CharField(max_length=100, blank=True)
    treatment = models.CharField(max_length=100, blank=True)
    farm = models.ForeignKey('Farm', related_name='animals')
    species = models.ForeignKey('animals.Species', related_name='chickens')

    def __str__(self):
        return self.animal_id

    @cached_property
    def relatives(self):
        targets = [r.target for r in self.source.all()]
        sources = [r.source for r in self.target.all()]
        return targets + sources

    @cached_property
    def parents(self):
        return [r.source for r in self.target.filter(relationship='PA')]

    @cached_property
    def children(self):
        return [r.target for r in self.source.filter(relationship='PA')]

    @cached_property
    def siblings(self):
        s1 = [r.target for r in self.source.exclude(relationship='PA')]
        s2 = [r.source for r in self.target.exclude(relationship='PA')]
        return s1 + s2


class Relatedness(models.Model):
    RELATIONSHIPS = (
        ('PA', 'parent'),
        ('SI', 'sibling'),
        ('HS', 'half-sibling'),
        ('MH', 'maternal half-sibling'),
        ('PH', 'paternal half-sibling'),
    )

    source = models.ForeignKey('Animal', related_name='source')
    target = models.ForeignKey('Animal', related_name='target')
    relationship = models.CharField(max_length=2, choices=RELATIONSHIPS)

    class Meta:
        unique_together = ('source', 'target')

    def __str__(self):
        if self.relationship == 'PA':
            return '{} is {} of {}'.format(
                self.source,
                self.get_parent_sex(),
                self.target
            )
        else:
            return '{} and {} are {}s'.format(
                self.source,
                self.target,
                self.get_relationship_display()
            )

    def get_parent_sex(self):
        if self.source.animal_sex == 'F':
            return 'mother'
        elif self.source_animal_sex == 'M':
            return 'father'
        else:
            return 'parent'


class Sampling(models.Model):
    FAT_STATUS = (
        ('L', 'low'),
        ('M', 'medium'),
        ('H', 'high'),
    )

    date = models.DateField(null=True, blank=True)
    colon_length = models.DecimalField(
        'colon length (cm)',
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )
    caecum_length = models.DecimalField(
        'caecum length (cm)',
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )
    fat_status = models.CharField(
        'Status of fat on the colon and caecum',
        max_length=1,
        choices=FAT_STATUS,
        blank=True
    )
    caecal_parasites = models.CharField(max_length=100, blank=True)
    other_observations = models.CharField(max_length=100, blank=True)
    estimated_age = models.PositiveSmallIntegerField(
        'estimated age (months)',
        null=True,
        blank=True
    )
    weight = models.DecimalField(
        'weight (kg)',
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True
    )
    animal = models.OneToOneField('Animal', related_name='sampling')
