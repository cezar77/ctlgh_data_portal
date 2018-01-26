from django.views.generic import DetailView

from django_filters.views import FilterView
from django_tables2.views import SingleTableView

from dataportal.modules.animals.models import Species
from .models import Population, Sampling, Animal
from .tables import SamplingTable, AnimalTable
from .filters import SamplingFilter, AnimalFilter


class SamplingList(FilterView, SingleTableView):
    model = Sampling
    table_class = SamplingTable
    template_name = 'sheep/sampling_list.html'

    filterset_class = SamplingFilter


class AnimalList(FilterView, SingleTableView):
    model = Animal
    table_class = AnimalTable
    template_name = 'core/table.html'

    filterset_class = AnimalFilter

    def get_context_data(self, **kwargs):
        context = super(AnimalList, self).get_context_data(**kwargs)
        context['species'] = Species.objects.get(slug='ovis-aries')
        return context


class AnimalDetail(DetailView):
    model = Animal
    context_object_name = 'animal'
