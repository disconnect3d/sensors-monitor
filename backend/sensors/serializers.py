from django.contrib.auth.models import User
from rest_framework import serializers
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
    class Meta:
        model = Sensor
        fields = ('id', 'host', 'kind', 'registered_at')


class MeasurementValueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MeasurementValue
        fields = ('id', 'sensor', 'value', 'measurement_time', 'upload_time', 'complex_id')


class ComplexMeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComplexMeasurement
        fields = ('id', 'sensor', 'name', 'begin', 'end', 'time_window', 'frequency', 'owner')
