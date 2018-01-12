from django.db import models
from django.utils.text import slugify


class Study(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.CharField(max_length=255, db_index=True)
    contact_person = models.ForeignKey('Person', related_name='studies')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(Study, self).save(*args, **kwargs)


class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.email)
