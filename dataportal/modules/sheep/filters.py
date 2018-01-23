import django_filters as filters

from .models import Sampling


class SamplingFilter(filters.FilterSet):
    class Meta:
        model = Sampling
        fields = ('date', 'site', 'longitude', 'latitude',
            'population__mean_litter_size', 'population__tail_type',
            'population__possible_related_breed')
