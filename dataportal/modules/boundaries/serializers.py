from rest_framework import serializers

from .models import Country


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Country
        fields = '__all__'
        extra_kwargs = {
            'url': {
                'lookup_field': 'iso',
                'view_name': 'boundaries:country-detail'
            }
        }
