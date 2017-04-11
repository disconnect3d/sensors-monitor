from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UsersTests(APITestCase):
    def test_add_user(self):
        """
        Ensure we can create a user object.
        """
        url = reverse("user-list")
        data = {
            "username": "test",
            "email": "test@test.pl"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')