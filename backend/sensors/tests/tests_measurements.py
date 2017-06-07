# from collections import OrderedDict
#
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from sensors.models import SensorKind, Host, Sensor, ComplexMeasurement
# from django.contrib.auth.models import User
#
# USER_CREDENTIALS = { 'username':"user", "password":"password"}
#
# class MeasurementTests(APITestCase):
#     def setUp(self):
#         SensorKind.objects.create(kind_name="kind")
#         Host.objects.create(name="host")
#         Sensor.objects.create(host=Host.objects.get(name="host"), kind=SensorKind.objects.get(kind_name="kind"))
#         User.objects.create_user(**USER_CREDENTIALS)
#
#         self.client.login(**USER_CREDENTIALS)
#
#     def test_can_add_complexMeasurement(self):
#         """
#         Ensure we can add new measurement
#         """
#
#         url = reverse('sensor-complex-list', kwargs={'pk': 1})
#
#         data = {
#             "name": "CPU on 1st January",
#             "begin": "2017-01-01 00:00",
#             "end": "2017-01-01 23:59",
#             "time_window": "60",
#             "frequency": "spo60",
#         }
#
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(ComplexMeasurement.objects.count(), 1)
