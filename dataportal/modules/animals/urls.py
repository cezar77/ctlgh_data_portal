from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'species', views.SpeciesViewSet)
router.register(r'image', views.ImageViewSet)

app_name = 'animals'
urlpatterns = [
    url(r'^', include(router.urls)),
]
