import django_filters as filters

from .models import Sampling


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
