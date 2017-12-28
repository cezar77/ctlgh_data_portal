from django.db import models
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.html import format_html


class Species(models.Model):
    common_name = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )
    slug = models.SlugField(max_length=50, db_index=True)
    species = models.CharField(max_length=30)
    genus = models.CharField(max_length=30)
    subfamily = models.CharField(max_length=30, blank=True)
    family = models.CharField(max_length=30)
    order = models.CharField(max_length=30)
    class_name = models.CharField('class', db_column='class', max_length=30)
    phylum = models.CharField(max_length=30)
    ncbi_id = models.PositiveSmallIntegerField('NCBI ID', unique=True)

    class Meta:
        verbose_name = 'Species'
        verbose_name_plural = 'Species'
        ordering = ('genus', 'species')

    def __str__(self):
        return '{} ({})'.format(self.common_name, self.binomial_name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.binomial_name)
        super(Species, self).save(*args, **kwargs)

    @cached_property
    def binomial_name(self):
        return '{} {}'.format(self.genus, self.species)

    NCBI_TAXONOMY_BASE_URL = 'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi'

    @cached_property
    def ncbi_taxonomy_url(self):
        return '{ncbi}?id={id}'.format(
            ncbi=self.NCBI_TAXONOMY_BASE_URL,
            id=self.ncbi_id
        )
        
    @cached_property
    def ncbi_taxonomy_html(self):
        return format_html(
            '<a href="{url}">{id}</a>', url=self.ncbi_taxonomy_url, id=self.ncbi_id
        )
    ncbi_taxonomy_html.short_description = 'NCBI Taxonomy URL'

