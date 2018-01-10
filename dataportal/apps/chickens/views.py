from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Farm


class FarmDetail(DetailView):
    model = Farm


class FarmCreate(CreateView):
    model = Farm
    fields = ['latitude', 'longitude', 'altitude', 'village', 'soil_type',
              'vegetation_type', 'agroecology', 'rainfall_pattern',
              'water_source', 'coop_type', 'previous_illness_occurence',
              'chicken_feed', 'other_animals']
