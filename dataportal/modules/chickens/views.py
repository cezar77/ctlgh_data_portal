from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django_filters.views import FilterView
from django_tables2.views import SingleTableView

from dataportal.modules.animals.models import Species
from .models import Animal
from .tables import AnimalTable
from .filters import AnimalFilter


class AnimalList(FilterView, SingleTableView):
    model = Animal
    table_class = AnimalTable
    template_name = 'core/table.html'

    filterset_class = AnimalFilter

    def get_context_data(self, **kwargs):
        context = super(AnimalList, self).get_context_data(**kwargs)
        context['species'] = Species.objects.get(slug='gallus-gallus')
        return context


class AnimalDetail(DetailView):
    model = Animal
    context_object_name = 'animal'
