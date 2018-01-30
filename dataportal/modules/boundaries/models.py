from django.contrib.gis.db import models
from django.utils.functional import cached_property
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation
)

from .apps import BoundariesConfig


class Country(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    iso = models.CharField(max_length=3)
    name_english = models.CharField(max_length=50)
    name_iso = models.CharField(max_length=54)
    name_fao = models.CharField(max_length=50)
    name_local = models.CharField(max_length=54)
    name_obsolete = models.CharField(max_length=150)
    name_variants = models.CharField(max_length=160)
    name_nonlatin = models.CharField(max_length=50)
    name_french = models.CharField(max_length=50)
    name_spanish = models.CharField(max_length=50)
    name_russian = models.CharField(max_length=50)
    name_arabic = models.CharField(max_length=50)
    name_chinese = models.CharField(max_length=50)
    waspartof = models.CharField(max_length=100)
    contains = models.CharField(max_length=50)
    sovereign = models.CharField(max_length=40)
    iso2 = models.CharField(max_length=4)
    www = models.CharField(max_length=2)
    fips = models.CharField(max_length=6)
    ison = models.FloatField()
    validfr = models.CharField(max_length=12)
    validto = models.CharField(max_length=10)
    pop2000 = models.FloatField()
    sqkm = models.FloatField()
    popsqkm = models.FloatField()
    unregion1 = models.CharField(max_length=254)
    unregion2 = models.CharField(max_length=254)
    developing = models.FloatField()
    cis = models.FloatField()
    transition = models.FloatField()
    oecd = models.FloatField()
    wbregion = models.CharField(max_length=254)
    wbincome = models.CharField(max_length=254)
    wbdebt = models.CharField(max_length=254)
    wbother = models.CharField(max_length=254)
    ceeac = models.FloatField()
    cemac = models.FloatField()
    ceplg = models.FloatField()
    comesa = models.FloatField()
    eac = models.FloatField()
    ecowas = models.FloatField()
    igad = models.FloatField()
    ioc = models.FloatField()
    mru = models.FloatField()
    sacu = models.FloatField()
    uemoa = models.FloatField()
    uma = models.FloatField()
    palop = models.FloatField()
    parta = models.FloatField()
    cacm = models.FloatField()
    eurasec = models.FloatField()
    agadir = models.FloatField()
    saarc = models.FloatField()
    asean = models.FloatField()
    nafta = models.FloatField()
    gcc = models.FloatField()
    csn = models.FloatField()
    caricom = models.FloatField()
    eu = models.FloatField()
    can = models.FloatField()
    acp = models.FloatField()
    landlocked = models.FloatField()
    aosis = models.FloatField()
    sids = models.FloatField()
    islands = models.FloatField()
    ldc = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    objects = models.GeoManager()

    class Meta:
        ordering = ('name_english',)
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name_english


class AdministrativeRouter(models.Model):
    limit = models.Q(app_label='sheep', model='sampling') | models.Q(app_label='chickens', model='farm')

    sampling_content_type = models.ForeignKey(
        'contenttypes.ContentType',
        related_name='%(app_label)s_%(class)s_sampling',
        limit_choices_to=limit
    )
    sampling_object_id = models.PositiveIntegerField(db_index=True)
    sampling = GenericForeignKey(
        'sampling_content_type',
        'sampling_object_id'
    )

    adm_content_type = models.ForeignKey(
        'contenttypes.ContentType',
        related_name='%(app_label)s_%(class)s_admarea',
        limit_choices_to={'app_label': 'boundaries'}
    )
    adm_object_id = models.PositiveIntegerField(db_index=True)
    administrative_area = GenericForeignKey(
        'adm_content_type',
        'adm_object_id'
    )

    def __str__(self):
        return '{} - {}'.format(
            self.sampling,
            self.administrative_area
        )


class AdministrativeArea(models.Model):
    id_0 = models.IntegerField()
    iso = models.CharField(max_length=3)
    name_0 = models.CharField(max_length=75)
    id_1 = models.IntegerField()
    name_1 = models.CharField(max_length=75)
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        abstract = True 


class FirstAdministrativeLevelManager(models.GeoManager):
    def get_by_natural_key(self, iso, id_1):
        return self.get(iso=iso, id_1=id_1)


class FirstAdministrativeLevel(AdministrativeArea):
    country = models.ForeignKey(
        'Country',
        related_name='first_administrative_level'
    )
    hasc_1 = models.CharField(
        verbose_name='Hierarchical administrative subdivision code',
        max_length=15
    )
    ccn_1 = models.IntegerField()
    cca_1 = models.CharField(max_length=254)
    type_1 = models.CharField(max_length=50)
    engtype_1 = models.CharField(max_length=50)
    nl_name_1 = models.CharField(max_length=50)
    varname_1 = models.CharField(max_length=150)
    router = GenericRelation(
        AdministrativeRouter,
        content_type_field='adm_content_type',
        object_id_field='adm_object_id',
        related_query_name='adm_areas1'
    )

    objects = FirstAdministrativeLevelManager()

    class Meta:
        db_table = '{}_admlevel1'.format(BoundariesConfig.name)
        unique_together = (('id_0', 'id_1'),)
        ordering = ('id_1',)
        verbose_name = '1st level administrative area'
        verbose_name_plural = '1st level administrative areas'

    def __str__(self):
        return '{}, {}'.format(self.name_1, self.name_0)

    def natural_key(self):
        return (self.iso, self.id_1)

    @cached_property
    def fake_id(self):
        return '{}.{}'.format(self.id_0, self.id_1)


class SecondAdministrativeLevelManager(models.GeoManager):
    def get_by_natural_key(self, iso, id_1, id_2):
        return self.get(iso=iso, id_1=id_1, id_2=id_2)


class SecondAdministrativeLevel(AdministrativeArea):
    country = models.ForeignKey(
        'Country',
        related_name='second_administrative_level'
    )
    adm_1 = models.ForeignKey(
        'FirstAdministrativeLevel',
        related_name='second_administrative_level',
        null=True,
        blank=True
    )
    id_2 = models.IntegerField()
    name_2 = models.CharField(max_length=75)
    hasc_2 = models.CharField(max_length=15)
    ccn_2 = models.IntegerField()
    cca_2 = models.CharField(max_length=254)
    type_2 = models.CharField(max_length=50)
    engtype_2 = models.CharField(max_length=50)
    nl_name_2 = models.CharField(max_length=75)
    varname_2 = models.CharField(max_length=150)
    router = GenericRelation(
        AdministrativeRouter,
        content_type_field='adm_content_type',
        object_id_field='adm_object_id',
        related_query_name='adm_areas2'
    )

    objects = SecondAdministrativeLevelManager()

    class Meta:
        db_table = '{}_admlevel2'.format(BoundariesConfig.name)
        unique_together = (('id_0', 'id_1', 'id_2'),)
        ordering = ('id_0', 'id_1', 'id_2',)
        verbose_name = '2nd level administrative area'
        verbose_name_plural = '2nd level administrative areas'

    def __str__(self):
        return '{}, {}, {}'.format(self.name_2, self.name_1, self.name_0)

    def natural_key(self):
        return (self.iso, self.id_1, self.id_2)

    @cached_property
    def fake_id(self):
        return '{}.{}.{}'.format(self.id_0, self.id_1, self.id_2)

    def save_foreign_key_for_first_level(self):
        self.adm_1 = FirstAdministrativeLevel.objects.get(
            id_0=self.id_0,
            id_1=self.id_1
        )
        self.save()


class ThirdAdministrativeLevelManager(models.GeoManager):
    def get_by_natural_key(self, iso, id_1, id_2, id_3):
        return self.get(iso=iso, id_1=id_1, id_2=id_2, id_3=id_3)

class ThirdAdministrativeLevel(AdministrativeArea):
    country = models.ForeignKey(
        'Country',
        related_name='third_administrative_level'
    )
    adm_1 = models.ForeignKey(
        'FirstAdministrativeLevel',
        related_name='third_administrative_level',
        null=True,
        blank=True
    )
    adm_2 = models.ForeignKey(
        'SecondAdministrativeLevel',
        related_name='third_administrative_level',
        null=True,
        blank=True
    )
    id_2 = models.IntegerField()
    name_2 = models.CharField(max_length=75)
    id_3 = models.IntegerField()
    name_3 = models.CharField(max_length=75)
    ccn_3 = models.IntegerField()
    cca_3 = models.CharField(max_length=15)
    type_3 = models.CharField(max_length=50)
    engtype_3 = models.CharField(max_length=50)
    nl_name_3 = models.CharField(max_length=75)
    varname_3 = models.CharField(max_length=100)
    router = GenericRelation(
        AdministrativeRouter,
        content_type_field='adm_content_type',
        object_id_field='adm_object_id',
        related_query_name='adm_areas3'
    )

    objects = ThirdAdministrativeLevelManager()

    class Meta:
        db_table = '{}_admlevel3'.format(BoundariesConfig.name)
        unique_together = (('id_0', 'id_1', 'id_2', 'id_3'),)
        ordering = ('id_0', 'id_1', 'id_2', 'id_3')
        verbose_name = '3rd level administrative area'
        verbose_name_plural = '3rd level administrative areas'

    def __str__(self):
        return '{}, {}, {}, {}'.format(
                self.name_3,
                self.name_2,
                self.name_1,
                self.name_0
            )

    def natural_key(self):
        return (self.iso, self.id_1, self.id_2, self.id_3)

    @cached_property
    def fake_id(self):
        return '{}.{}.{}.{}'.format(self.id_0, self.id_1, self.id_2, self.id_3)

    def save_foreign_key_for_first_level(self):
        self.adm_1 = FirstAdministrativeLevel.objects.get(
            id_0=self.id_0,
            id_1=self.id_1
        )
        self.save()

    def save_foreign_key_for_second_level(self):
        self.adm_2 = SecondAdministrativeLevel.objects.get(
            id_0=self.id_0,
            id_1=self.id_1,
            id_2=self.id_2
        )
        self.save()


class FourthAdministrativeLevelManager(models.GeoManager):
    def get_by_natural_key(self, iso, id_1, id_2, id_3, id_4):
        return self.get(iso=iso, id_1=id_1, id_2=id_2, id_3=id_3, id_4=id_4)


class FourthAdministrativeLevel(AdministrativeArea):
    country = models.ForeignKey(
        'Country',
        related_name='fourth_administrative_level'
    )
    adm_1 = models.ForeignKey(
        'FirstAdministrativeLevel',
        related_name='fourth_administrative_level',
        null=True,
        blank=True
    )
    adm_2 = models.ForeignKey(
        'SecondAdministrativeLevel',
        related_name='fourth_administrative_level',
        null=True,
        blank=True
    )
    id_2 = models.IntegerField()
    name_2 = models.CharField(max_length=75)
    adm_3 = models.ForeignKey(
        'ThirdAdministrativeLevel',
        related_name='fourth_administrative_level',
        null=True,
        blank=True
    )
    id_3 = models.IntegerField()
    name_3 = models.CharField(max_length=75)
    id_4 = models.IntegerField()
    name_4 = models.CharField(max_length=100)
    varname_4 = models.CharField(max_length=100)
    ccn_4 = models.IntegerField()
    cca_4 = models.CharField(max_length=20)
    type_4 = models.CharField(max_length=35)
    engtype_4 = models.CharField(max_length=35)
    router = GenericRelation(
        AdministrativeRouter,
        content_type_field='adm_content_type',
        object_id_field='adm_object_id',
        related_query_name='adm_areas4'
    )

    objects = FourthAdministrativeLevelManager()

    class Meta:
        db_table = '{}_admlevel4'.format(BoundariesConfig.name)
        unique_together = (('id_0', 'id_1', 'id_2', 'id_3', 'id_4'),)
        ordering = ('id_0', 'id_1', 'id_2', 'id_3', 'id_4')
        verbose_name = '4th level administrative area'
        verbose_name_plural = '4th level administrative areas'

    def __str__(self):
        return '{}, {}, {}, {}, {}'.format(
                self.name_4,
                self.name_3,
                self.name_2,
                self.name_1,
                self.name_0
            )

    def natural_key(self):
        return (self.iso, self.id_1, self.id_2, self.id_3, self.id_4)

    @cached_property
    def fake_id(self):
        return '{}.{}.{}.{}.{}'.format(
                self.id_0,
                self.id_1,
                self.id_2,
                self.id_3,
                self.id_4
            )

    def save_foreign_key_for_first_level(self):
        self.adm_1 = FirstAdministrativeLevel.objects.get(
            id_0=self.id_0,
            id_1=self.id_1
        )
        self.save()

    def save_foreign_key_for_second_level(self):
        self.adm_2 = SecondAdministrativeLevel.objects.get(
            id_0=self.id_0,
            id_1=self.id_1,
            id_2=self.id_2
        )
        self.save()

    def save_foreign_key_for_third_level(self):
        self.adm_3 = ThirdAdministrativeLevel.objects.get(
            id_0=self.id_0,
            id_1=self.id_1,
            id_2=self.id_2,
            id_3=self.id_3
        )
        self.save()


class FifthAdministrativeLevelManager(models.GeoManager):
    def get_by_natural_key(self, iso, id_1, id_2, id_3, id_4, id_5):
        return self.get(iso=iso, id_1=id_1, id_2=id_2, id_3=id_3, id_4=id_4, id_5=id_5)


class FifthAdministrativeLevel(AdministrativeArea):
    country = models.ForeignKey(
        'Country',
        related_name='fifth_administrative_level'
    )
    adm_1 = models.ForeignKey(
        'FirstAdministrativeLevel',
        related_name='fifth_administrative_level',
        null=True,
        blank=True
    )
    adm_2 = models.ForeignKey(
        'SecondAdministrativeLevel',
        related_name='fifth_administrative_level',
        null=True,
        blank=True
    )
    id_2 = models.IntegerField()
    name_2 = models.CharField(max_length=75)
    adm_3 = models.ForeignKey(
        'ThirdAdministrativeLevel',
        related_name='fifth_administrative_level',
        null=True,
        blank=True
    )
    id_3 = models.IntegerField()
    name_3 = models.CharField(max_length=75)
    adm_4 = models.ForeignKey(
        'FourthAdministrativeLevel',
        related_name='fifth_administrative_level',
        null=True,
        blank=True
    )
    id_4 = models.IntegerField()
    name_4 = models.CharField(max_length=100)
    id_5 = models.IntegerField()
    name_5 = models.CharField(max_length=75)
    ccn_5 = models.IntegerField()
    cca_5 = models.CharField(max_length=25)
    type_5 = models.CharField(max_length=25)
    engtype_5 = models.CharField(max_length=25)
    router = GenericRelation(
        AdministrativeRouter,
        content_type_field='adm_content_type',
        object_id_field='adm_object_id',
        related_query_name='adm_areas5'
    )

    objects = FifthAdministrativeLevelManager()

    class Meta:
        db_table = '{}_admlevel5'.format(BoundariesConfig.name)
        unique_together = (('id_0', 'id_1', 'id_2', 'id_3', 'id_4', 'id_5'),)
        ordering = ('id_0', 'id_1', 'id_2', 'id_3', 'id_4', 'id_5')
        verbose_name = '5th level administrative area'
        verbose_name_plural = '5h level administrative areas'

    def __str__(self):
        return '{}, {}, {}, {}, {}, {}'.format(
                self.name_5,
                self.name_4,
                self.name_3,
                self.name_2,
                self.name_1,
                self.name_0
            )

    def natural_key(self):
        return (self.iso, self.id_1, self.id_2, self.id_3, self.id_4, self.id_5)

    @cached_property
    def fake_id(self):
        return '{}.{}.{}.{}.{}.{}'.format(
                self.id_0,
                self.id_1,
                self.id_2,
                self.id_3,
                self.id_4,
                self.id_5
            )

    def save_foreign_key_for_first_level(self):
        self.adm_1 = FirstAdministrativeLevel.objects.get(
            id_0=self.id_0,
            id_1=self.id_1
        )
        self.save()

    def save_foreign_key_for_second_level(self):
        self.adm_2 = SecondAdministrativeLevel.objects.get(
            id_0=self.id_0,
            id_1=self.id_1,
            id_2=self.id_2
        )
        self.save()

    def save_foreign_key_for_third_level(self):
        self.adm_3 = ThirdAdministrativeLevel.objects.get(
            id_0=self.id_0,
            id_1=self.id_1,
            id_2=self.id_2,
            id_3=self.id_3
        )
        self.save()

    def save_foreign_key_for_fourth_level(self):
        self.adm_4 = FourthAdministrativeLevel.objects.get(
            id_0=self.id_0,
            id_1=self.id_1,
            id_2=self.id_2,
            id_3=self.id_3,
            id_4=self.id_4
        )
        self.save()
