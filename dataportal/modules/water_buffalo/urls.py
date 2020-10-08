from django.conf.urls import url

from . import views
from .apps import WaterBuffaloConfig


app_name = WaterBuffaloConfig.name
urlpatterns = [
    url(r'^$', views.AnimalList.as_view(), name='animal-list'),
]

