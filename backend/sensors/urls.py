"""sensors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from rest_framework import routers

from sensors import views

# http://www.django-rest-framework.org/api-guide/routers/
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^hosts/$', views.HostList.as_view(), name='host-list'),
    url(r'^hosts/(?P<pk>[0-9]+)/$', views.HostDetail.as_view(), name='host-detail'),
    url(r'^hosts/(?P<pk>[0-9]+)/sensors/$', views.HostSensorsList.as_view(), name='host-sensor-list'),
    url(r'^sensors/$', views.SensorList.as_view(), name='sensor-list'),
    url(r'^sensors/(?P<pk>[0-9]+)/$', views.SensorDetail.as_view(), name='sensor-detail'),
    url(r'^sensors/(?P<pk>[0-9]+)/measurements/$', views.SensorMeasurementsList.as_view(), name='sensor-measurement-list'),
    url(r'^sensors/(?P<pk2>[0-9]+)/measurements/(?P<pk>[0-9]+)/$', views.SensorMeasurementsDetail.as_view(), name='sensor-measurement-detail'),

    url(r'^sensors/(?P<pk>[0-9]+)/complex-measurements/$', views.SensorComplexMeasurementsList.as_view(),
        name='sensor-complex-list'),


    url(r'^sensor_kinds/$', views.SensorKindList.as_view(), name='sensorkind-list'),
    url(r'^sensor_kinds/(?P<pk>[0-9]+)/$', views.SensorKindDetail.as_view(), name='sensorkind-detail'),
]
