import re
import urllib

from django.db import models
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.html import format_html
from django.urls import reverse


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
    image = models.OneToOneField(
        'Image',
        on_delete=models.CASCADE,
        related_name='species'
    )
    app = models.OneToOneField(
        'contenttypes.ContentType',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name='species'
    )

    class Meta:
        verbose_name = 'Species'
        verbose_name_plural = 'Species'
        ordering = ('genus', 'species')

    def __str__(self):
        return '{} ({})'.format(self.common_name, self.binomial_name)

    def get_absolute_url(self):
        return reverse('animals:species-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.binomial_name)
        super(Species, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Species, self).delete(*args, **kwargs)        

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

    @cached_property
    def display_image(self):
        return format_html(
            '<figure><img src="{file_url}" alt="{alt}" width="512"><figcaption>{attribution}</figcaption></figure>',
            file_url=self.image.file_url,
            alt=self.image,
            attribution=format_html(self.image.attribution)
        )

    @property
    def species_homepage(self):
        app_label = self.app.app_label
        return reverse('{}:animal-list'.format(app_label))


class Image(models.Model):
    page_url = models.URLField('Page URL', max_length=255, unique=True)
    file_url = models.URLField('File URL', max_length=255, unique=True)
    attribution = models.CharField(max_length=500)

    def __str__(self):
        m = re.match(r'^.+/(.+)\.jpg$', self.file_url)
        result = m.group(1)
        return urllib.parse.unquote(result.replace('_', ' '))

    def get_absolute_url(self): 
        return reverse('image-detail', kwargs={'pk': str(self.pk)})

    @cached_property
    def display_image(self):
        return self.species.display_image
