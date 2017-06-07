from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

USER_CREDENTIALS = {'username': "user", "password": "password", "email": "a@b.com"}


class UsersTests(APITestCase):
    def setUp(self):
        User.objects.create_user(**USER_CREDENTIALS)
        self.client.login(**USER_CREDENTIALS)

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
        self.assertEqual(User.objects.count(), 2) # because of user created in setup
        self.assertEqual(User.objects.last().username, 'test')
