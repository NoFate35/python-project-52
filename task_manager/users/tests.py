from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UsersTest(TestCase):
    fixtures = ["users.json"]

    def test_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_fixtures(self):
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, "rrr")
    
    def test_users_list(self):
        response = self.client.get(reverse("users_list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("users", response.context)
        users = response.context["users"]

        self.assertTrue(len(users) == 3)

    def test_user_create(self):
        create_url = reverse("users_create")
        list_url = reverse("users_list")
        self.client.post(create_url, data={"first_name": "Bobik", "last_name": 'S', 'username': 'bob-S', 'password1':'123', 'password2':'123'})
        response = self.client.get(list_url)
        self.assertContains(response, "Bobik")
        users = response.context["users"]
        self.assertTrue(len(users) == 4)