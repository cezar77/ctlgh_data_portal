import django_filters as filters

from .models import Sampling, Animal
from .forms import AnimalFilterForm


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

    class Meta:
        model = Animal
        fields = ('animal_sex', 'sampling__date',
            'sampling__population__mean_litter_size',
            'sampling__population__possible_related_breed',
            'sampling__population__tail_type',
            'sampling__population__tail_shape', 'sampling__site'
        )

    def __init__(self, *args, **kwargs):
        super(AnimalFilter, self).__init__(*args, **kwargs)
        self.filters['sampling__population__tail_type'].label = 'Tail type'
        self.filters['sampling__population__tail_shape'].label = 'Tail shape'
