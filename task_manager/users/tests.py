from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse


class UsersTest(TestCase):
    def test_users_list(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)