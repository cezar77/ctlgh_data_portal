from django.conf.urls import url

from . import views
from .apps import ChickensConfig

app_name = ChickensConfig.name
urlpatterns = [
    #url(r'^$', views.FarmList.as_view(), name='farm-list'),
    url(r'^farm/(?P<pk>[\d]+)/$', views.FarmDetail.as_view(), name='farm-detail'),
    url(r'^farm/new/$', views.FarmCreate.as_view(), name='farm-create'),
    url(r'^$', views.AnimalList.as_view(), name='animal-list'),
    url(r'^(?P<pk>\d+)/$', views.AnimalDetail.as_view(), name='animal-detail'),
]
