from django.conf.urls import url

from . import views
from .apps import SheepConfig

app_name = SheepConfig.name
urlpatterns = [
    url(r'^$', views.AnimalList.as_view(), name='animal-list'),
    url(r'(?P<pk>\d+)/$', views.AnimalDetail.as_view(), name='animal-detail'),
    url(r'^sampling/$', views.SamplingList.as_view(), name='sampling-list'),
]
