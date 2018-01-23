from django_filters.views import FilterView
from django_tables2.views import SingleTableView

from .models import Population, Sampling, Animal
from .tables import SamplingTable
from .filters import SamplingFilter


class SamplingList(FilterView, SingleTableView):
    model = Sampling
    table_class = SamplingTable
    filterset_class = SamplingFilter
    template_name = 'sheep/sampling_list.html'
