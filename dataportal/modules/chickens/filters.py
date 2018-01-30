import django_filters as filters

from dataportal.modules.boundaries.models import Country
from .models import Animal


class AnimalFilter(filters.FilterSet):
    sampling__weight = filters.RangeFilter(
        label='Weight range',
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
    farm__village = filters.CharFilter(
        label='Village',
        lookup_expr='icontains'
    )
    farm__agroecology = filters.CharFilter(
        label='Agroecology',
        lookup_expr='icontains'
    )
    country = filters.ModelChoiceFilter(
        name='country',
        label='Country',
        queryset=Country.objects.all(),
        method='country_filter'
    )

    class Meta:
        model = Animal
        fields = ('animal_sex', 'sampling__weight', 'farm__village',
            'farm__agroecology', 'country')

    def country_filter(self, queryset, name, value):
        qs1 = queryset.filter(farm__administrative_area__adm_areas1__country=value)
        qs2 = queryset.filter(farm__administrative_area__adm_areas2__country=value)
        qs3 = queryset.filter(farm__administrative_area__adm_areas3__country=value)
        qs4 = queryset.filter(farm__administrative_area__adm_areas4__country=value)
        qs5 = queryset.filter(farm__administrative_area__adm_areas5__country=value)
        return qs5.union(qs4, qs3, qs2, qs1)

