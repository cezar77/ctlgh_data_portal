import django_filters as filters

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
        widget=filters.widgets.RangeWidget(
            attrs={'placeholder': 'YYYY-MM-DD'}
        )
    )
    sampling__population__mean_litter_size = filters.RangeFilter(
        widget=filters.widgets.RangeWidget(
            attrs={
                'type': 'number',
                'step': 0.01,
                'min': 0,
                'max': 10
            }
        )
    )

    class Meta:
        model = Animal
        fields = ('animal_sex', 'sampling__date',
            'sampling__population__mean_litter_size',
            'sampling__population__tail_type',
            'sampling__population__tail_shape', 'sampling__site'
        )
