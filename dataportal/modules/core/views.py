from django.views.generic import ListView

from dataportal.modules.animals.models import Species


class HomeView(ListView):
    model = Species
    context_object_name = 'species'
    template_name = 'core/home.html'
