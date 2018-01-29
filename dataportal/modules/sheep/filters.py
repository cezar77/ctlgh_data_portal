from django.db.models import Q

import django_filters as filters

from dataportal.modules.boundaries.models import Country, AdministrativeRouter
from .models import Sampling, Animal


class SamplingFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(
        widget=filters.widgets.RangeWidget(
            attrs={'placeholder': 'YYYY-MM-DD'}
        )
    )
    population__mean_litter_size = filters.RangeFilter()

    class Meta:
        model = Sampling
        fields = ('date', 'site',
            'population__mean_litter_size', 'population__tail_type',
            'population__possible_related_breed')


class AnimalFilter(filters.FilterSet):
    sampling__date = filters.DateFromToRangeFilter(
        label='Between the dates',
        widget=filters.widgets.RangeWidget(
            attrs={
                'class': 'datepicker',
                'style': 'width:8em;'
            }
        )
    )
    sampling__population__mean_litter_size = filters.RangeFilter(
        label='Mean litter size range',
        widget=filters.widgets.RangeWidget(
            attrs={
                'type': 'number',
                'step': 0.01,
                'min': 0,
                'max': 10,
                'style': 'width:5em;'
            }
        )
    )
    sampling__population__possible_related_breed = filters.CharFilter(
        label='Breed',
        lookup_expr='icontains'
    )
    sampling__altitude = filters.NumericRangeFilter(
        label='Altitudinal range',
        widget=filters.widgets.RangeWidget(
            attrs={
                'type': 'number',
                'step': 1,
                'min': 0,
                'max': 10000,
                'style': 'width:5em;'
            }
        ),
        lookup_expr='overlap'
    )
    country = filters.ModelChoiceFilter(
        name='country',
        label='Country',
        queryset=Country.objects.all(),
        method='country_filter'
    )

    class Meta:
        model = Animal
        fields = ('animal_sex', 'sampling__date',
            'sampling__population__mean_litter_size',
            'sampling__population__possible_related_breed',
            'sampling__population__tail_type',
            'sampling__population__tail_shape', 'sampling__site',
            'country'
        )

    def __init__(self, *args, **kwargs):
        super(AnimalFilter, self).__init__(*args, **kwargs)
        self.filters['sampling__population__tail_type'].label = 'Tail type'
        self.filters['sampling__population__tail_shape'].label = 'Tail shape'

    def country_filter(self, queryset, name, value):
        qs1 = queryset.filter(sampling__administrative_area__adm_areas1__country=value)
        qs2 = queryset.filter(sampling__administrative_area__adm_areas2__country=value)
        qs3 = queryset.filter(sampling__administrative_area__adm_areas3__country=value)
        qs4 = queryset.filter(sampling__administrative_area__adm_areas4__country=value)
        qs5 = queryset.filter(sampling__administrative_area__adm_areas5__country=value)
        return qs5.union(qs4, qs3, qs2, qs1)

