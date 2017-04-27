from django.contrib.auth.models import User
from django.db import models


class SensorKind(models.Model):
    kind_name = models.CharField(max_length=64)

    def __str__(self):
        return self.kind_name


class Host(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    kind = models.ForeignKey(SensorKind)
    registered_at = models.DateTimeField()

    def __str__(self):
        return "{}@{} [{}]".format(self.kind.kind_name, self.host.name, self.registered_at)


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

    def __str__(self):
        return "'{}' (owner: {}) : sensor {}, start: {}, end: {}, time window: {} s, freq: {} s".format(
            self.name, self.owner, self.sensor, self.begin, self.end, self.time_window, self.frequency)


class MeasurementValue(models.Model):
    """ Represents single measured value. API will return array of these. If complex_id is None, then it is measured 
    value. Otherwise, it is calculated and part of complex measurement """
    sensor = models.ForeignKey(Sensor)
    value = models.FloatField()
    measurement_time = models.DateTimeField()
    upload_time = models.DateTimeField()
    complex_id = models.ForeignKey(ComplexMeasurement, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Measurement for sensor {} : value = {}, measured on {}, uploaded on {}, calculated: {}".format(
            self.sensor, self.value, self.measurement_time, self.upload_time,
            ('false' if self.complex_id is None else 'true'))

    @property
    def complex(self):
        return self.complex_id is not None
