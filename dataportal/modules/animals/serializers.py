from rest_framework import serializers

from .models import Species, Image


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    species = serializers.HyperlinkedRelatedField(
        view_name='species-detail',
        read_only=True,
        lookup_field='slug'
    )

    class Meta:
        model = Image
        fields = (
            'url', 'id', 'page_url', 'file_url', 'attribution', 'species'
        )
        extra_kwargs = {
            'page_url': {'validators': []},
            'file_url': {'validators': []}
        }


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(required=True)

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

    def create(self, validated_data):
        image_data = validated_data.pop('image')
        image = ImageSerializer.create(ImageSerializer(), validated_data=image_data) 
        species = Species.objects.create(image=image, **validated_data)
        return species

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image')
        image = instance.image

        instance.common_name = validated_data.get('common_name', instance.common_name)
        instance.species = validated_data.get('species', instance.species)
        instance.genus = validated_data.get('genus', instance.genus)
        instance.subfamily = validated_data.get('subfamily', instance.subfamily)
        instance.family = validated_data.get('family', instance.family)
        instance.order = validated_data.get('order', instance.order)
        instance.class_name = validated_data.get('class_name', instance.class_name)
        instance.phylum = validated_data.get('phylum', instance.phylum)
        instance.ncbi_id = validated_data.get('ncbi_id', instance.ncbi_id)
        instance.save()

        image.page_url = image_data.get('page_url', image.page_url)
        image.file_url = image_data.get('file_url', image.file_url)
        image.attribution = image_data.get('attribution', image.attribution)
        image.save()

        return instance

SpeciesSerializer._declared_fields['class'] = serializers.CharField(source='class_name')
