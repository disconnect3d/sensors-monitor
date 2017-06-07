from collections import OrderedDict
from datetime import date

from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase

from sensors.models import SensorKind, Host, Sensor, ComplexMeasurement, MeasurementValue
from django.contrib.auth.models import User

USER_CREDENTIALS = {'username': "user", "password": "password"}


class MeasurementTests(APITestCase):
    def setUp(self):
        SensorKind.objects.create(kind_name="kind")
        self.host = Host.objects.create(name="host")
        self.sensor = Sensor.objects.create(host=Host.objects.get(name="host"),
                                            kind=SensorKind.objects.get(kind_name="kind"))
        self.user = User.objects.create_user(**USER_CREDENTIALS)

        self.client.login(**USER_CREDENTIALS)

    def test_can_get_complex_measurements(self):
        ComplexMeasurement.objects.create(name="test", begin=now(), end=now(), time_window=60, frequency=60,
                                          sensor=self.sensor, owner=self.user)

        ComplexMeasurement.objects.create(name="test2", begin=now(), end=now(), time_window=60, frequency=60,
                                          sensor=self.sensor, owner=self.user)

        url = reverse('sensor-complex-list', kwargs={'pk': 1})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_can_add_complex_measurement(self):
        """
        Ensure we can add new measurement
        """

        url = reverse('sensor-complex-list', kwargs={'pk': 1})

        measurement_name = "CPU on 1st January";
        data = {
            "name": measurement_name,
            "begin": "2017-01-01 00:00",
            "end": "2017-01-01 23:59",
            "time_window": "60",
            "frequency": "60",
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ComplexMeasurement.objects.count(), 1)
        self.assertEqual(ComplexMeasurement.objects.get().name, measurement_name)

    def test_can_delete_complex_measurement(self):
        url = reverse('sensor-complex-list', kwargs={'pk': 1})

        complex = ComplexMeasurement.objects.create(name="test", begin=now(), end=now(), time_window=60, frequency=60,
                                                    sensor=self.sensor, owner=self.user)

        MeasurementValue.objects.create(sensor=self.sensor, value=1, measurement_time=now(), complex_id=complex)

        data = {"id": "1"}

        response = self.client.delete(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ComplexMeasurement.objects.count(), 0)
        self.assertEqual(MeasurementValue.objects.count(), 0)

    def test_can_put_complex_measurement(self):
        url = reverse('sensor-complex-list', kwargs={'pk': 1})

        measurement = ComplexMeasurement.objects.create(name="test", begin=now(), end=now(), time_window=60,
                                                        frequency=60, sensor=self.sensor, owner=self.user)

        new_name = "new name"
        data = measurement.__dict__
        data['name'] = new_name

        response = self.client.put(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ComplexMeasurement.objects.count(), 1)
        self.assertEqual(ComplexMeasurement.objects.get().name, new_name)
