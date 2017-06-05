from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

from .models import SensorKind, Host, Sensor, ComplexMeasurement, MeasurementValue, User
from .serializers import UserSerializer, SensorKindSerializer, HostSerializer, SensorSerializer, \
    ComplexMeasurementSerializer, MeasurementValueSerializer, MeasurementsListSimplifiedSerializer


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


class SensorKindList(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    List sensor kinds, create or update one.
    """
    queryset = SensorKind.objects.all()
    serializer_class = SensorKindSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SensorKindDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve, update or delete a sensor kind.
    """
    queryset = SensorKind.objects.all()
    serializer_class = SensorKindSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class HostSensorsList(APIView):
    """
    List sensors for given host, create or update a sensor.
    """
    def get(self, request, pk, format=None):
        try:
            host = Host.objects.get(pk=pk)
        except Host.DoesNotExist:
            raise Http404
        sensors = host.sensor_set.all()
        serializer = SensorSerializer(sensors, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """#FIXME probably this can be written in a better and safer way"""
        serializer = HostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorList(mixins.ListModelMixin, generics.GenericAPIView):
    """
    Retrieve sensor list.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SensorDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve or delete a sensor.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SensorMeasurementsList(APIView):
    """
    List measurements for given sensor or create one.
    """
    def get(self, request, pk, format=None):
        try:
            sensor = Sensor.objects.get(pk=pk)
        except Sensor.DoesNotExist:
            raise Http404
        measurements = sensor.measurementvalue_set.all()
        serializer = MeasurementsListSimplifiedSerializer(measurements, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """#FIXME probably this can be written in a better and safer way"""
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorMeasurementsDetail(mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Delete a measurement.
    """
    queryset = MeasurementValue.objects.all()
    serializer_class = MeasurementValueSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
