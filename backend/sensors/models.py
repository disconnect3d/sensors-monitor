import hashlib
import uuid

from django.db import models


class SensorKind(models.Model):
    kind_name = models.CharField(max_length=64)


class Sensor(models.Model):
    hostname = models.CharField(max_length=64)
    kind = models.ForeignKey(SensorKind)
    registered_at = models.DateTimeField


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor)
    value = models.FloatField
    measurement_time = models.DateTimeField
    upload_time = models.DateTimeField


class User(models.Model):
    """ Class representing user in system."""
    name = models.CharField(max_length=32)
    password = models.CharField
    salt = models.CharField
    created_at = models.DateTimeField

    def hash_password(self, password):
        """ Returns hash of given password using self.salt. """
        return hashlib.sha512(password + self.salt).hexdigest()

    def password_match(self, password_to_check):
        """ Checks if given password matches the one stored in database, useful in log-in logic """
        return self.password == self.hash_password(password_to_check)

    def set_password(self, password):
        """ Sets new password for user """
        self.salt = uuid.uuid4()
        self.password = self.hash_password(password)

    def __init__(self, password="password"):
        """ Creates user with given password, which is automatically hashed. Default password is 'password'
        """
        self.set_password(password)


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
    begin = models.DateTimeField
    end = models.DateTimeField
    time_window = models.BigIntegerField
    frequency = models.BigIntegerField
    owner = models.ForeignKey(User)
