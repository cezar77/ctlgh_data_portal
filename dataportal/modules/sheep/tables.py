import django_tables2 as tables

from .models import Sampling


class SamplingTable(tables.Table):
    class Meta:
        model = Sampling
        template = 'django_tables2/bootstrap.html'
        fields = ('date', 'site', 'longitude', 'latitude', 'altitude',
            'locality', 'population', 'administrative_area')
