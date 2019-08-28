"""dataportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('dataportal.modules.core.urls')),
    url(r'^animals/', include('dataportal.modules.animals.urls')),
    url(r'^sheep/', include('dataportal.modules.sheep.urls')),
    url(r'^chickens/', include('dataportal.modules.chickens.urls')),
    url(r'^boundaries/', include('dataportal.modules.boundaries.urls')),
    url(r'^ideal/', include('ideal.urls')),
    url(r'^ideal/', include('ideal.helper.urls')),
]
