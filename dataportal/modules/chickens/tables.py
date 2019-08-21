from django.utils.html import format_html

import django_tables2 as tables
from django_tables2 import A

from dataportal.modules.core.templatetags import lonlat
from .models import Animal


class AnimalTable(tables.Table):
    id = tables.LinkColumn(
        viewname='chickens:animal-detail',
        kwargs={'pk': A('pk')},
        accessor='animal_id',
        orderable=False
    )
    animal_sex = tables.Column()
    administrative_area = tables.ManyToManyColumn(
        verbose_name='Administrative Area',
        accessor='farm.administrative_area',
        orderable=True,
        transform=lambda ar: ar.administrative_area
    )
    longitude = tables.Column(
        verbose_name='Longitude',
        accessor='farm.longitude'
    )
    latitude = tables.Column(
        verbose_name='Latitude',
        accessor='farm.latitude'
    )
    altitude = tables.Column(
        verbose_name='Altitude',
        accessor='farm.altitude_display',
        order_by='farm.altitude'
    )
    export_formats = ['tsv']

    class Meta:
        model = Animal
        fields = ('id', 'animal_sex', 'sampling.weight', 'farm.village',
            'farm.agroecology', 'longitude', 'latitude', 'altitude',
            'administrative_area'
        )
        attrs = {
            'class': 'table table-responsive table-hover'
        }

    def render_animal_sex(self, value):
        html = '<i class="fa{fa}"></i>'
        if value == 'female':
            fa_class = ' fa-venus'
        elif value == 'male':
            fa_class = ' fa-mars'
        else:
            fa_class = ''
        return format_html(html, fa=fa_class)

    def value_animal_sex(self, value):
        return value

    def render_longitude(self, value):
        return lonlat.longitude(value)

    def render_latitude(self, value):
        return lonlat.latitude(value)

    def value_altitude(self, record):
        return record.farm.altitude

    def order_administrative_area(self, queryset, is_descending):
        return (queryset.order_by(
            ('-' if is_descending else '') + 'farm__administrative_area'
        ), True)
