from django.contrib.auth.models import User
from django.db import models


class SensorKind(models.Model):
    kind_name = models.CharField(max_length=64)


class Sensor(models.Model):
    hostname = models.CharField(max_length=64)
    kind = models.ForeignKey(SensorKind)
    registered_at = models.DateTimeField()


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor)
    value = models.FloatField()
    measurement_time = models.DateTimeField()
    upload_time = models.DateTimeField()


class ComplexMeasurement(models.Model):
    """
    Represents complex measurement
    
    sensor - data source and data type
    name - name of measurement
    begin, end - time span of measurement
    time_window - time span for average value calculation, in seconds
    frequency - frequency of values calculated from time_window, in seoonds
    owner - user who created complex measurement
    """
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    time_window = models.BigIntegerField()
    frequency = models.BigIntegerField()
    owner = models.ForeignKey(User)
