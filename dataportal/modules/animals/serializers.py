import json

from django.contrib.contenttypes.models import ContentType
from django.core import serializers as sr

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Species, Image


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    species = serializers.HyperlinkedRelatedField(
        view_name='animals:species-detail',
        read_only=True,
        lookup_field='slug'
    )

    class Meta:
        model = Image
        fields = (
            'url', 'id', 'page_url', 'file_url', 'attribution', 'species'
        )
        extra_kwargs = {
            'url': {'view_name': 'animals:image-detail'},
            'page_url': {'validators': []},
            'file_url': {'validators': []}
        }

    def validate_page_url(self, value):
        if self.context['request']._request.method == 'POST':
            unique = UniqueValidator(
                self.Meta.model.objects.all(),
                message='Image with this page URL already exists.'
            )
            unique.set_context(self.fields['page_url'])
            unique(value)
        return value

    def validate_file_url(self, value):
        if self.context['request']._request.method == 'POST':
            unique = UniqueValidator(
                self.Meta.model.objects.all(),
                message='Image with this file URL already exists.'
            )
            unique.set_context(self.fields['file_url'])
            unique(value)
        return value


class AppRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance.natural_key()

    def to_representation(self, value):
        return json.dumps(value.natural_key())

    def to_internal_value(self, data):
        data = json.loads(data)
        return ContentType.objects.get(
            app_label=data[0],
            model=data[1]
        )


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    app = AppRelatedField(
        queryset=ContentType.objects.all(),
        many=False,
        allow_null=True,
        required=False
    )
    image = ImageSerializer(required=True)

    class Meta:
        model = Species
        fields = (
            'url', 'id', 'common_name', 'slug',  'species', 'genus',
            'subfamily', 'family', 'order', 'class', 'phylum',
            'ncbi_id', 'ncbi_taxonomy_url', 'app',  'image',
        )
        depth = 1
        read_only_fields = ('slug',)
        extra_kwargs = {
            'url': {
                'lookup_field': 'slug',
                'view_name': 'animals:species-detail'
            }
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
        instance.app = validated_data.get('app', instance.app)
        instance.save()

        image.page_url = image_data.get('page_url', image.page_url)
        image.file_url = image_data.get('file_url', image.file_url)
        image.attribution = image_data.get('attribution', image.attribution)
        image.save()

        return instance

SpeciesSerializer._declared_fields['class'] = serializers.CharField(source='class_name')
