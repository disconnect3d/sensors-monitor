from collections import OrderedDict

from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase

from sensors.models import SensorKind, Host, Sensor

NUMBER_OF_SENSORS = 10


class SensorTests(APITestCase):
    def setUp(self):
        SensorKind.objects.create(kind_name="kind1")
        SensorKind.objects.create(kind_name="kind2")
        Host.objects.create(name="host1")
        Host.objects.create(name="host2")

    def test_cant_add_sensor(self):
        """
        Ensure we can't create a sensor object.
        """
        url = reverse("sensor-list")
        data = {
            "host": {
                "id": 1
            },
            "kind": {
                "id": 1
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Sensor.objects.count(), 0)

    def test_get_sensors_list(self):
        """
        Ensure we can get a sensors list.
        """
        host1 = Host.objects.get(name="host1")
        kind1 = SensorKind.objects.get(kind_name="kind1")
        for i in range(NUMBER_OF_SENSORS):
            Sensor.objects.create(host=host1,
                                  kind=kind1,
                                  registered_at=now())
        url = reverse("sensor-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), NUMBER_OF_SENSORS)

    def test_get_sensor(self):
        """
        Ensure we can get a sensor object.
        """
        registered_at = now()
        host1 = Host.objects.get(name="host1")
        kind1 = SensorKind.objects.get(kind_name="kind1")
        Sensor.objects.create(host=host1,
                              kind=kind1,
                              registered_at=registered_at)
        sensor_id = Sensor.objects.get().id
        url = reverse("sensor-detail", kwargs={'pk': sensor_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["registered_at"], registered_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(response.data["host"], OrderedDict([('id', host1.id), ('name', host1.name)]))
        self.assertEqual(response.data["kind"], OrderedDict([('id', kind1.id), ('kind_name', kind1.kind_name)]))

    def test_cant_remove_sensor(self):
        """
        Ensure we can remove a sensor object.
        """
        registered_at = now()
        host1 = Host.objects.get(name="host1")
        kind1 = SensorKind.objects.get(kind_name="kind1")
        Sensor.objects.create(host=host1,
                              kind=kind1,
                              registered_at=registered_at)
        sensor_id = Sensor.objects.get().id
        url = reverse("sensor-detail", kwargs={'pk': sensor_id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sensor.objects.count(), 0)
