from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import SensorKind, Host, Sensor, MeasurementValue, ComplexMeasurement


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups')


class SensorKindSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = SensorKind
        fields = ('id', 'kind_name',)


class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host
        fields = ('id', 'name',)


class SensorSerializer(serializers.HyperlinkedModelSerializer):
    host = HostSerializer()
    kind = SensorKindSerializer()

    class Meta:
        model = Sensor
        fields = ('id', 'host', 'kind', 'registered_at')
        extra_kwargs = {'url': {'view_name': 'rest_framework:host-sensor-list'}}


class MeasurementValueSerializer(serializers.HyperlinkedModelSerializer):
    sensor = SensorSerializer()

    class Meta:
        model = MeasurementValue
        fields = ('id', 'sensor', 'value', 'measurement_time', 'upload_time', 'complex_id')


class ComplexMeasurementSerializer(serializers.HyperlinkedModelSerializer):
    sensor = PrimaryKeyRelatedField(queryset=Sensor.objects.all(), required=False)
    owner = PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = ComplexMeasurement
        fields = ('id', 'sensor', 'name', 'begin', 'end', 'time_window', 'frequency', 'owner')


class MeasurementsListSimplifiedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MeasurementValue
        fields = ('value', 'measurement_time')
