from django.views.generic.detail import DetailView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django_filters.views import FilterView
from django_tables2.views import SingleTableView
from django_tables2.export.views import ExportMixin

from dataportal.modules.animals.models import Species
from .models import Animal
from .tables import AnimalTable
from .filters import AnimalFilter


@method_decorator(cache_page(30*24*60*60), name='dispatch')
class AnimalList(ExportMixin, FilterView, SingleTableView):
    model = Animal
    table_class = AnimalTable
    template_name = 'core/table.html'
    filterset_class = AnimalFilter
    export_name = 'chickens'

    def get_context_data(self, **kwargs):
        context = super(AnimalList, self).get_context_data(**kwargs)
        context['species'] = Species.objects.get(slug='gallus-gallus')
        return context


@method_decorator(cache_page(30*24*60*60), name='dispatch')
class AnimalDetail(DetailView):
    model = Animal
    context_object_name = 'animal'
