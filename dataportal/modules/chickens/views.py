from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django_tables2.views import SingleTableView

from dataportal.modules.animals.models import Species
from .models import Farm, Animal
from .tables import AnimalTable


class FarmList(ListView):
    model = Farm


class FarmDetail(DetailView):
    model = Farm


class FarmCreate(CreateView):
    model = Farm
    fields = ['latitude', 'longitude', 'altitude', 'village', 'soil_type',
              'vegetation_type', 'agroecology', 'rainfall_pattern',
              'water_source', 'coop_type', 'previous_illness_occurence',
              'chicken_feed', 'other_animals']

class AnimalList(SingleTableView):
    model = Animal
    table_class = AnimalTable
    template_name = 'core/table.html'

    def get_context_data(self, **kwargs):
        context = super(AnimalList, self).get_context_data(**kwargs)
        context['species'] = Species.objects.get(slug='gallus-gallus')
        return context


class AnimalDetail(DetailView):
    model = Animal
    context_object_name = 'animal'
