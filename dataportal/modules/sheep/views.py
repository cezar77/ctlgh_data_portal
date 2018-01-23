from django.views.generic import ListView

from .models import Population, Sampling, Animal


class SamplingList(ListView):
    model = Sampling
    context_object_name = 'samplings'
