from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views
from .apps import AnimalsConfig

router = DefaultRouter()
router.register(r'species', views.SpeciesViewSet)
router.register(r'image', views.ImageViewSet)

app_name = AnimalsConfig.name
urlpatterns = [
    url(r'^', include(router.urls)),
]
