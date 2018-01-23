from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sampling/$', views.SamplingList.as_view(), name='sampling-list'),
]
