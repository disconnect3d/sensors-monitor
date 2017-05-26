from random import random, randint

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from sensors.models import Host

NUMBER_OF_HOSTS = 10


class HostTests(APITestCase):
    def test_add_host(self):
        """
        Ensure we can create a host object.
        """
        url = reverse("host-list")
        data = {
            "name": "test"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Host.objects.get().name, 'test')
        self.assertEqual(Host.objects.count(), 1)

    def test_add_many_hosts(self):
        """
        Ensure we can create many host objects.
        """
        url = reverse("host-list")

        for i in range(NUMBER_OF_HOSTS):
            data = {
                "name": "test" + str(i)
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Host.objects.count(), i + 1)

    def test_get_hosts_list(self):
        """
        Ensure we can get a hosts list.
        """
        url = reverse("host-list")
        for i in range(NUMBER_OF_HOSTS):
            Host.objects.create(name="test" + str(i))

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), NUMBER_OF_HOSTS)

    def test_get_host(self):
        """
        Ensure we can get a host object.
        """
        Host.objects.create(name="test")
        host_id = Host.objects.get().id
        url = reverse("host-detail", kwargs={'pk': host_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': Host.objects.get().id, 'name': 'test'})

    def test_get_non_existent_host(self):
        """
        Ensure we can get non-existent host object.
        """
        host_id = randint(0, 100)
        url = reverse("host-detail", kwargs={'pk': host_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_host(self):
        """
        Ensure we can update a host object.
        """
        Host.objects.create(name="test")
        host_id = Host.objects.get().id
        url = reverse("host-detail", kwargs={'pk': host_id})
        data = {
            "name": "updated_test"
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Host.objects.get().name, 'updated_test')
        self.assertEqual(Host.objects.count(), 1)

    def test_remove_host(self):
        """
        Ensure we can remove a host object.
        """
        Host.objects.create(name="test")
        host_id = Host.objects.get().id
        url = reverse("host-detail", kwargs={'pk': host_id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Host.objects.count(), 0)
