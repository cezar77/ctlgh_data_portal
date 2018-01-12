from rest_framework import serializers

from .models import Species, Image


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Species
        fields = (
            'url', 'id', 'common_name', 'slug',  'species', 'genus',
            'subfamily', 'family', 'order', 'class', 'phylum',
            'ncbi_id', 'ncbi_taxonomy_url', 'image'
        )
        depth = 1
        read_only_fields = ('slug',)
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

SpeciesSerializer._declared_fields['class'] = serializers.CharField(source='class_name')


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = (
            'url', 'id', 'page_url', 'file_url', 'attribution'
        )
