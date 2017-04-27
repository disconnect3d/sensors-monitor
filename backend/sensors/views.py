from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets

from .models import SensorKind, Host, Sensor, ComplexMeasurement, MeasurementValue, User
from .serializers import UserSerializer, SensorKindSerializer, HostSerializer, SensorSerializer, \
    ComplexMeasurementSerializer, MeasurementValueSerializer

from rest_framework import mixins
from rest_framework import generics


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class HostList(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    List hosts, create or update a host.
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class HostDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve, update or delete a host instance.
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)