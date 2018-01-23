from django_tables2 import SingleTableView

from .models import Population, Sampling, Animal
from .tables import SamplingTable


class SamplingList(SingleTableView):
    model = Sampling
    table_class = SamplingTable
