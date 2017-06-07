from random import randint

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from sensors.models import SensorKind

NUMBER_OF_SENSOR_KINDS = 10
USER_CREDENTIALS = {'username': "user", "password": "password", "email": "a@b.com"}


class SensorsKindTests(APITestCase):
    def setUp(self):
        User.objects.create_user(**USER_CREDENTIALS)
        self.client.login(**USER_CREDENTIALS)

    def test_add_sensorKind(self):
        """
        Ensure we can create a sensorKind object.
        """
        url = reverse("sensorkind-list")
        data = {
            "kind_name": "test"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SensorKind.objects.get().kind_name, 'test')
        self.assertEqual(SensorKind.objects.count(), 1)

    def test_add_many_sensorKinds(self):
        """
        Ensure we can create many sensorKind objects.
        """
        url = reverse("sensorkind-list")

        for i in range(NUMBER_OF_SENSOR_KINDS):
            data = {
                "kind_name": "test" + str(i)
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(SensorKind.objects.count(), i + 1)

    def test_get_sensorKind_list(self):
        """
        Ensure we can get a sensorKinds list.
        """
        url = reverse("sensorkind-list")
        for i in range(NUMBER_OF_SENSOR_KINDS):
            SensorKind.objects.create(kind_name="test" + str(i))

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), NUMBER_OF_SENSOR_KINDS)

    def test_get_sensorKind(self):
        """
        Ensure we can get a sensorKind object.
        """
        SensorKind.objects.create(kind_name="test")
        sensorKind_id = SensorKind.objects.get().id
        url = reverse("sensorkind-detail", kwargs={'pk': sensorKind_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': SensorKind.objects.get().id, 'kind_name': 'test'})

    def test_get_non_existent_sensorKind(self):
        """
        Ensure we can't get non-existent sensorKind object.
        """
        sensorKind_id = randint(0, 100)
        url = reverse("sensorkind-detail", kwargs={'pk': sensorKind_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_sensorKind(self):
        """
        Ensure we can remove a sensorKind object.
        """
        SensorKind.objects.create(kind_name="test")
        sensorKind_id = SensorKind.objects.get().id
        url = reverse("sensorkind-detail", kwargs={'pk': sensorKind_id})
        data = {
            "kind_name": "updated_test"
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SensorKind.objects.get().kind_name, 'updated_test')
        self.assertEqual(SensorKind.objects.count(), 1)

    def test_update_sensorKind(self):
        """
        Ensure we can update a sensorKind object.
        """
        SensorKind.objects.create(kind_name="test")
        sensorKind_id = SensorKind.objects.get().id
        url = reverse("sensorkind-detail", kwargs={'pk': sensorKind_id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SensorKind.objects.count(), 0)
