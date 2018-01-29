from django.utils.html import format_html

import django_tables2 as tables
from django_tables2 import A

from .models import Sampling, Animal


class SamplingTable(tables.Table):
    administrative_area = tables.Column(orderable=False)

    class Meta:
        model = Sampling
        template = 'django_tables2/bootstrap.html'
        fields = ('date', 'site', 'longitude', 'latitude', 'altitude',
            'locality', 'population', 'administrative_area')


class AnimalTable(tables.Table):
    id = tables.LinkColumn(
        viewname='sheep:animal-detail',
        kwargs={'pk': A('pk')},
        accessor='animal_id',
        orderable=False
    )
    animal_sex = tables.Column()
    administrative_area = tables.ManyToManyColumn(
        verbose_name='Administrative Area',
        accessor='sampling.administrative_area',
        orderable=True,
        transform=lambda ar: ar.administrative_area
    )
    altitude = tables.Column(
        verbose_name='Altitude',
        accessor='sampling.altitude_display',
        order_by='sampling.altitude'
    )

    class Meta:
        model = Animal
        template = 'django_tables2/bootstrap.html'
        fields = (
            'id', 'animal_sex', 'sampling.date',
            'sampling.population.possible_related_breed',
            'sampling.population.mean_litter_size',
            'sampling.population.tail_type',
            'sampling.population.tail_shape',
            'sampling.site', 'sampling.locality', 'altitude'
        )

    def render_animal_sex(self, value):
        html = '<i class="fa{fa}"></i>'
        if value == 'female':
            fa_class = ' fa-venus'
        elif value == 'male':
            fa_class = ' fa-mars'
        else:
            fa_class = ''
        return format_html(html, fa=fa_class)
