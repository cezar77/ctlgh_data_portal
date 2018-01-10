from django.conf.urls import url

from .views import FarmList, FarmDetail, FarmCreate

urlpatterns = [
    url(r'^$', FarmList.as_view(), name='farm-list'),
    url(r'^farm/(?P<pk>[\d]+)/$', FarmDetail.as_view(), name='farm-detail'),
    url(r'^farm/new/$', FarmCreate.as_view(), name='farm-create'),
]
