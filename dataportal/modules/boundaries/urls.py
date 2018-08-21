from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views
from .apps import BoundariesConfig

router = DefaultRouter()
router.register(r'country', views.CountryViewSet)

app_name = BoundariesConfig.name
urlpatterns = [
    url(r'^', include(router.urls)),
]
