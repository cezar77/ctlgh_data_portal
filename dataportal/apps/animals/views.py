from rest_framework import viewsets

from .models import Species
from .serializers import SpeciesSerializer


class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    lookup_field = 'slug'

