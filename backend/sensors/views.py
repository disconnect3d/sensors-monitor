from django.http import Http404
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SensorKind, Host, Sensor, ComplexMeasurement, MeasurementValue
from .serializers import SensorKindSerializer, HostSerializer, SensorSerializer, \
    ComplexMeasurementSerializer, MeasurementValueSerializer, MeasurementsListSimplifiedSerializer


class HostList(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    List hosts, create or update a host.
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SensorKindDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    """
    Retrieve, update or delete a sensor kind.
    """
    queryset = SensorKind.objects.all()
    serializer_class = SensorKindSerializer
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SensorDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve or delete a sensor.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SensorMeasurementsList(APIView):
    """
    List measurements for given sensor or create one.
    """
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        try:
            sensor = Sensor.objects.get(pk=pk)
        except Sensor.DoesNotExist:
            raise Http404

        from_datetime = self.request.query_params.get('from_datetime', None)
        to_datetime = self.request.query_params.get('to_datetime', None)

        measurements = sensor.measurementvalue_set

        if from_datetime:
            measurements = measurements.filter(measurement_time__gt=from_datetime)

        if to_datetime:
            measurements = measurements.filter(measurement_time__lt=to_datetime)

        serializer = MeasurementsListSimplifiedSerializer(measurements, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """#FIXME probably this can be written in a better and safer way"""
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorComplexMeasurementsList(APIView):
    """
    List complex measurements definitions for given sensor or create one.
    Does not contain mesaurement data
    """

    def get(self, request, pk, format=None):
        try:
            sensor = Sensor.objects.get(pk=pk)
        except Sensor.DoesNotExist:
            raise Http404

        measurements = sensor.complexmeasurement_set.all()
        serializer = ComplexMeasurementSerializer(measurements, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        try:
            sensor = Sensor.objects.get(pk=pk)
        except Sensor.DoesNotExist:
            raise Http404
        serializer = ComplexMeasurementSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data["sensor_id"] = sensor.id
            serializer.validated_data["owner_id"] = request.user.id

            measurement = serializer.save()

            self._calculate_values_for_complex_measurement(measurement)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            sensor = Sensor.objects.get(pk=pk)
            measurement = ComplexMeasurement.objects.get(id=request.data["id"], owner_id=request.user.id)
            measurement.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Sensor.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        try:
            sensor = Sensor.objects.get(pk=pk)
            measurement = ComplexMeasurement.objects.get(id=request.data["id"], owner_id=request.user.id)
        except Sensor.DoesNotExist:
            raise Http404
        except ComplexMeasurement.DoesNotExist:
            raise Http404

        serializer = ComplexMeasurementSerializer(data=request.data, instance=measurement)

        if serializer.is_valid():
            serializer.save()

            # delete all old values
            MeasurementValue.objects.filter(complex_id=measurement).delete()

            # calculate new ones
            self._calculate_values_for_complex_measurement(measurement)

            return Response(serializer.data, status=status.HTTP_200_OK)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _calculate_values_for_complex_measurement(self, complex_measurement):
        pass


class SensorMeasurementsDetail(mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Delete a measurement.
    """
    queryset = MeasurementValue.objects.all()
    serializer_class = MeasurementValueSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
