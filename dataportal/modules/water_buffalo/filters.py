import django_filters as filters

from .models import Animal


class AnimalFilter(filters.FilterSet):
    breed = filters.ChoiceFilter(
        label='Breed',
        choices=Animal.BREEDS,
    )

    class Meta:
        model = Animal
        fields = ('breed',)

