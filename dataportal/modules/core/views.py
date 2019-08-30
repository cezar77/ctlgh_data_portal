from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from dataportal.modules.animals.models import Species


@method_decorator(cache_page(30*24*60*60), name='dispatch')
class HomeView(ListView):
    model = Species
    context_object_name = 'species'
    template_name = 'core/home.html'
