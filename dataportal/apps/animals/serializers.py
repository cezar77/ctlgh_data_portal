from rest_framework import serializers

from .models import Species


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Species
        fields = (
            'url', 'id', 'common_name', 'slug',  'species', 'genus',
            'subfamily', 'family', 'order', 'class', 'phylum',
            'ncbi_id', 'ncbi_taxonomy',
        )
        read_only_fields = ('slug',)
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

SpeciesSerializer._declared_fields['class'] = serializers.CharField(source='class_name')
